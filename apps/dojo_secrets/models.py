from __future__ import unicode_literals
import bcrypt
from django.db import models

class UserManager(models.Manager):
    
    def validate(self, form):
        
        errors = []
        user_record = User.objects.filter(email=form['email']).first()
        if user_record:
            errors.append("Email already exists.")
            return errors

        if len(form['fname']) == 0 or len(form['lname']) == 0 or len(form['email']) == 0 or len(form['password']) == 0 or len(form['pwconfirm']) == 0:
            
            errors.append("Fields cannot be blank.")
            return errors
        
        if form['password'] != form['pwconfirm']:
            errors.append("Passwords do not match.")
            return errors
        
        return errors
    
    
    def register(self, form):

        errors = []
        
        password = str(form['password'])
        encryptedpw = bcrypt.hashpw(password, bcrypt.gensalt())
        
        user = User.objects.create(
                fname = form['fname'],
                lname = form['lname'],
                email = form['email'],
                password = encryptedpw,

            )
        return user

    
    def validate_login(self, form):
        print "Inside the login_validate method"

        
        errors = []
        user_check = User.objects.filter(email=form['email']).first()
        # print user_check
        if len(form['email']) == 0 or len(form['password']) == 0:
            errors.append("Fields cannot be blank.")
            return errors

        if user_check == None:
            errors.append("User not in database")
            return errors
    
        if user_check:
            password = str(form['password'])
            user_pass = str(user_check.password)

            encryptedpw = bcrypt.hashpw(password, user_pass)

            if encryptedpw == user_pass:
                return user_check
            
            errors.append("Invalid Password")
        
        return errors
    

class User(models.Model):
    fname = models.CharField(max_length = 50)
    lname = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 255)
    password = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s %s' %(self.fname, self.lname, self.email, self.password)

    objects = UserManager()

class SecretManager(models.Manager):
    def secret_validation(self, form):
        
        errors = []

        if len(form['content']) == 0:
            errors.append('Secret content is required.')
        
        return errors

    def create_secret(self, user, form):
        secret = Secret.objects.create(
                content = form['content'],
                user = user
            )
        return secret
        

class Secret(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name='secrets')
    liked_by = models.ManyToManyField(User, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SecretManager()
            
