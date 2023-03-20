from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User_issue
from .import db, tables_dict
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def transactions():
    # if request.method == 'POST':
    #     note = request.form.get('note')
    #     if len(note) < 1:
    #         flash("Note is too short!", category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash("Note added!", category='success')
    return render_template("transactions.html", user=current_user)

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
#     return jsonify({})


@views.route('/base-admin', methods=['GET','POST'])
@login_required
def admin_work():
    return render_template("admin_work.html",user=current_user, tables_dict = tables_dict )