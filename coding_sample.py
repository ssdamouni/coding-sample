@app.route('/users/<int:user_id>/add-instrument', methods=["GET","POST"])
def edit_user_instruments(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    if g.user and session[CURR_USER_KEY] != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    if g.user and session[CURR_USER_KEY] == user_id:
        instruments = Instrument.query.all()
        instrument_list = [(k.id, k.instrument) for k in instruments]
        form = UserInstrumentForm()
        form.instrument_id.choices = instrument_list
        if form.validate_on_submit():
            try:
                selected_instruments= form.instrument_id.data
                i = 0
                while i < len(selected_instruments):
                    user_instrument = UserInstrument(user_id=user_id, instrument_id=form.instrument_id.data[i])
                    db.session.add(user_instrument)
                    db.session.commit()
                    i+=1
                return redirect(f'/users/{user_id}')
            
            except IntegrityError:
                flash("You have already added one or more of these instruments", 'danger')
                return render_template('users/{user_id}/add-genre', form=form)
        return render_template('users/instrument-add.html', form=form)
