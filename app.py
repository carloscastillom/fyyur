#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

""" app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:sdvsf1989@localhost:5432/todoapp'

db=SQLAlchemy(app)
migrate = Migrate(app, db) 


  

    




"""
 


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genre = db.Column(db.String())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(),  default=False)
    seeking_description = db.Column(db.String)
    #artists = db.relationship('Artist', backref=db.backref('venue', lazy=True))
    artist = db.relationship('Artist',  secondary = 'Show', backref='venue')
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    #Genres

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genre = db.Column(db.String())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(),  default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Venue', secondary = 'Show', backref='artist')
    
#check this thing internet how to properly do a many ot many relationship
class Show(db.Model):
   __tablename__='Show'

   id = db.Column(db.Integer,primary_key=True)  
   venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
   artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
   start_date = db.Column(db.DateTime,nullable=False)



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():
#empty list. data we would like to retrieve for venues 
  data=[]

# Select disting cities from the venues
  cities = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state)

#
  for city in cities:
      venues_in_city = db.session.query(Venue.id, Venue.name).filter(Venue.city == city[0]).filter(Venue.state == city[1])
      data.append({
        "city": city[0],
        "state": city[1],
        "venues": venues_in_city
      })
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  results = Venue.query.filter(Venue.name.ilike('%{}%'.format(request.form['search_term']))).all()
  response={
    "count": len(results),
    "data": []
    }
  for venue in results:
    response["data"].append({
        "id": venue.id,
        "name": venue.name
      })
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = db.session.query(Venue).filter(Venue.id == venue_id).one()

  data ={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genre,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
  }

  return render_template('pages/show_venue.html', venue=data)


#======================I am here==========================

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  
  form = VenueForm(request.form)

  venue = Venue(
    name = form.name.data,
    city = form.city.data,
    state = form.state.data,
    genre = form.genres.data,
    address = form.address.data,
    phone = form.phone.data,
    website = form.website.data,
    facebook_link = form.facebook_link.data,
    seeking_talent = form.seeking_talent.data,
    seeking_description = form.seeking_description.data,
    image_link = form.image_link.data,
  )
  try:
      db.session.add(venue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + form.name.data + ' was successfully listed!')
  except:
      flash('An error occurred. Venue ' + form.name.data + ' could not be added.')
  finally:
      db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(id=venue_id).delete(venue_id)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('venues'))
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
 



#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  data=[]
  artist_loop = db.session.query(Artist.id, Artist.name)

  for a in artist_loop:
    data.append({
      'id': a[0],
      'name': a[1]
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  results =Artist.query.filter(Artist.name.ilike('%{}%'.format(request.form['search_term']))).all()
  response={
    'count': len(results),
    'data': []
  }
  for a in results:
    response['data'].append({
      'id': a.id,
      'name': a.name
    })

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  artist= db.session.query(Artist).filter(Artist.id == artist_id).one()

  data={
    'id': artist.id,
    'name':artist.name,
    'genres':artist.genre,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'website': artist.website,
    'facebook_link': artist.facebook_link, 
    'seeking_venue': artist.seeking_venue,
    'seeking_description': artist.seeking_description,
    'image_link': artist  .image_link,
    #past shows and upcoming shows    
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist= db.session.query(Artist).filter(Artist.id == artist_id).one()
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form=ArtistForm(request.form)
  artist= db.session.query(Artist).filter(Artist.id == artist_id).one()

  updated_aritst = {
      name: form.name.data,
      genres: form.genres.data,
      address: form.address.data,
      city: form.city.data,
      state: form.state.data,
      phone: form.phone.data,
      website: form.website.data,
      facebook_link: form.facebook_link.data,
      seeking_venue: form.seeking_venue.data,
      seeking_description: form.seeking_description.data,
      image_link: form.image_link.data,
    }
  try:
      db.session.query(Artist).filter(Artist.id == artist_id).update(updated_artist)
      db.session.commit()
      flash('Artist ' + form.name.data + ' was successfully listed!')
  except:
      flash('An error occurred. Artist ' + form.name.data + 'could not be added')
  finally:
      db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  form = VenueForm()
  venue = db.session.query(Venue).filter(Venue.id == venue_id).one()
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  venue = db.session.query(Venue).filter(Venue.id == venue_id).one()

  updated_venue = {
      name: form.name.data,
      genres: form.genres.data,
      address: form.address.data,
      city: form.city.data,
      state: form.state.data,
      phone: form.phone.data,
      website: form.website.data,
      facebook_link: form.facebook_link.data,
      seeking_talent: form.seeking_talent.data,
      seeking_description: form.seeking_description.data,
      image_link: form.image_link.data
    }

  try:
      db.session.query(Venue).filter(Venue.id == venue_id).update(updated_venue)
      db.session.commit()
      flash('Venue' + form.name.data + ' updated')
  except:
      flash('An error occurred. Venue ' + form.name.data + ' not updated')
  finally:
      db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)

  artist=Artist(
    name = form.name.data,
    genres = form.genres.data,
    city = form.city.data,
    phone = form.phone.data,
    website = form.website.data,
    facebook_link = form.facebook_link.data,
    seeking_venue = form.seeking_venue.data,
    seeking_description = form.seeking_description.data,
    image_link = form.image_link.data,
  )
  try:
     db.session.add(artist)
     db.session.commit()
     flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    flash(' Artist ' + request.form['name'] + 'could not be listed')
  finally:
    db.session.close()
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  data= []
  Shows = db.session.query(Show).all()

  for s in Shows:
      artist = db.session.query(Artist.name, Artist.image_link).filter(Artist.id == s[0]).one()
      venue = db.session.query(Venue.name).filter(Venue.id == s[1]).one()
      data.append({
          "venue_id": s[1],
          "venue_name": venue[0],
          "artist_id": s[0],
          "artist_name": artist[0],
          "artist_image_link": artist[1],
          "start_time": str(s[2])
      })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)

  show=Shows(
    show_id = form.show_id.data,
    venue_id = form.venue_id.data,
    artist_id = form.artist_id.data,
    start_date = form.start_date.data,
  )
  try:
     db.session.add(Shows)
     db.session.commit()
     flash(' Show was successfully listed! ')
  except:
    flash(' flash an error instead ')
  finally:
    db.session.close()
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')



  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
