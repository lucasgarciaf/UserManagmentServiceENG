import os
from flask import Flask, request, jsonify
from flasgger import Swagger
from models import User, Base
from database import SessionLocal, engine
from datetime import datetime


Base.metadata.create_all(engine)

app = Flask(__name__)

swagger = Swagger(app)


# Create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        description: User object
        required: true
        schema:
          type: object
          required:
            - name
            - birthdate
          properties:
            name:
              type: string
              description: User's full name [e.g. Lucas Garcia]
            birthdate:
              type: string
              format: date
              description: User's date of birth (YYYY-MM-DD) [e.g. 1991-10-01]
    responses:
      201:
        description: User created successfully
        schema:
          id: User
          properties:
            id:
              type: integer
            name:
              type: string
            birthdate:
              type: string
              format: date
            active:
              type: boolean
      400:
        description: Invalid input
    """
    session = SessionLocal()
    data = request.get_json()
    try:
        user = User(
            name=data['name'],
            birthdate=datetime.strptime(data['birthdate'], '%Y-%m-%d'),
            active=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return jsonify({
            'id': user.id,
            'name': user.name,
            'birthdate': user.birthdate.isoformat(),
            'active': user.active
        }), 201
    
    except Exception as e:
       session.rollback()
       session.close()
       return jsonify({'error': str(e)}), 400

# Update user state
@app.route('/api/users/<int:user_id>/state', methods=['PUT'])
def update_user_state(user_id):
    """
    Update user's active state
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID of the user to update
      - in: body
        name: body
        description: Active state data
        required: true
        schema:
          type: object
          required:
            - active
          properties:
            active:
              type: boolean
              description: New active state
    responses:
      206:
        description: User state updated successfully
        schema:
          id: User
          properties:
            id:
              type: integer
            active:
              type: boolean
      400:
        description: Invalid input
      404:
        description: User not found
    """
    session = SessionLocal()
    data = request.get_json()
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        try:
            user.active = data['active']
            session.commit()
            session.close()
            return  '', 204
        except Exception as e:
            session.rollback()
            session.close()
            return jsonify({'error': str(e)}), 400
    else:
        session.close()
        return jsonify({'error': 'User not found'}), 404

# Delete a user
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID of the user to delete
    responses:
      204:
        description: User deleted successfully
      404:
        description: User not found
    """
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
        session.close()
        return '', 204
    else:
        session.close()
        return jsonify({'error': 'User not found'}), 404

# List all active users
@app.route('/api/users/active', methods=['GET'])
def list_active_users():
    """
    List all active users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of active users
        schema:
          type: array
          items:
            $ref: '#/definitions/User'
    definitions:
      User:
        type: object
        properties:
          id:
            type: integer
          name:
            type: string
          birthdate:
            type: string
            format: date
          active:
            type: boolean
    """
    session = SessionLocal()
    users = session.query(User).filter(User.active == True).all()
    result = [{
        'id': user.id,
        'name': user.name,
        'birthdate': user.birthdate.isoformat(),
        'active': user.active
    } for user in users]
    session.close()
    return jsonify(result), 200

# List all inactive users
@app.route('/api/users/inactive', methods=['GET'])
def list_inactive_users():
    """
    List all inactive users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of inactive users
        schema:
          type: array
          items:
            $ref: '#/definitions/User'
    definitions:
      User:
        type: object
        properties:
          id:
            type: integer
          name:
            type: string
          birthdate:
            type: string
            format: date
          active:
            type: boolean
    """
    session = SessionLocal()
    users = session.query(User).filter(User.active == False).all()
    result = [{
        'id': user.id,
        'name': user.name,
        'birthdate': user.birthdate.isoformat(),
        'active': user.active
    } for user in users]
    session.close()
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
