from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user, login_required
import json
from website.models import Trip
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

#ruta pentru pagina cu calatoriile personale
@views.route('/mytrips', methods=['GET', 'POST'])
@login_required
def mytrips():
    if request.method == 'POST':
        start_location = request.form.get('start_location')
        end_location = request.form.get('end_location')
        story = request.form.get('story')

        if len(start_location) < 1:
            flash('The start location is too short!', category='error')
        elif len(end_location) < 1:
            flash('The end location is too short!', category='error')
        elif len(story) < 1:
            flash('The story is too short!', category='error')
        else:
            new_trip = Trip(start_location=start_location, 
                            end_location=end_location, 
                            story=story, 
                            user_id=current_user.id)
            db.session.add(new_trip)
            db.session.commit()
          
            flash('Trip added', category='success')
            

    return render_template("TripsPage.html", user=current_user)

@views.route('/all-trips')
def all_trips():
    #iau toate calatoriile din baza de date
    trips = Trip.query.all()
    return render_template('all_trips.html', trips=trips, user=current_user)

@views.route('/delete-trip', methods=['POST'])
def delete_note():
    trip = json.loads(request.data)
    tripId = trip['tripId']
    trip  = Trip.query.get(tripId)
    if trip:
        if trip.user_id == current_user.id:
            db.session.delete(trip)
            db.session.commit()
            
    return jsonify({})