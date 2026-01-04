import json
import os
import hashlib

class UserManager:
    def __init__(self, data_dir='data', filename='users.json'):
        self.filepath = os.path.join(data_dir, filename)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Creates the users file with default admin if it doesn't exist."""
        if not os.path.exists(self.filepath):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            # Default admin user
            initial_data = {
                "admin": {
                    "password": self._hash_password("admin123"),
                    "role": "admin",
                    "name": "System Admin"
                }
            }
            try:
                with open(self.filepath, 'w') as f:
                    json.dump(initial_data, f, indent=4)
            except IOError as e:
                print(f"Error creating user file: {e}")

    def _hash_password(self, password):
        """
        Hashes password. 
        WARNING: CHANGED TO PLAIN TEXT FOR ADMIN VISIBILITY REQUEST. 
        Revert to hashlib.sha256(password.encode()).hexdigest() for production.
        """
        return password

    def load_users(self):
        """Loads all users from JSON file."""
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def save_users(self, users):
        """Saves users dict to JSON file."""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(users, f, indent=4)
            return True
        except IOError:
            return False

    def authenticate(self, username, password):
        """Verifies username and password. Returns user dict if valid, else None."""
        users = self.load_users()
        user = users.get(username)
        if user and user['password'] == self._hash_password(password):
            user['username'] = username # Attach username to result for convenience
            return user
        return None

    def create_user(self, username, password, role, name="", **kwargs):
        """Creates a new user. Returns True if successful, False if username exists."""
        users = self.load_users()
        if username in users:
            return False
            
        users[username] = {
            "password": self._hash_password(password),
            "role": role,
            "name": name,
            **kwargs
        }
        return self.save_users(users)

    def get_user(self, username):
        """Gets a single user by username."""
        users = self.load_users()
        user = users.get(username)
        if user:
            user['username'] = username
        return user

    def update_user(self, username, **kwargs):
        """Updates user fields. Password should be hashed before passing if being updated via this raw method, 
           or use update_password specific method."""
        users = self.load_users()
        if username not in users:
            return False
        
        users[username].update(kwargs)
        return self.save_users(users)

    def delete_user(self, username):
        """Deletes a user."""
        users = self.load_users()
        if username in users:
            del users[username]
            return self.save_users(users)
        return False
        
    def reset_password(self, username, new_password):
        """Resets a user's password."""
        return self.update_user(username, password=self._hash_password(new_password))

    def get_users_by_role(self, role):
        """Returns a list of users with a specific role."""
        users = self.load_users()
        return {k: v for k, v in users.items() if v.get('role') == role}

    def rename_user(self, old_username, new_username):
        """Renames a user key."""
        users = self.load_users()
        if old_username not in users or new_username in users:
            return False
            
        users[new_username] = users.pop(old_username)
        # Assuming we might want to update the 'username' field inside the dict too if we rely on it
        # But our structure is {username: {data}}. If we use get_user it adds it.
        # Just in case we added it in update methods:
        if 'username' in users[new_username]:
             users[new_username]['username'] = new_username
             
        return self.save_users(users)
