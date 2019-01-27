from flask import Flask, render_template, redirect, request, url_for
import subprocess
import crypt
import random
import string

app = Flask(__name__)

#function to execute system command
def command_exec(cmd):
    check_output = subprocess.check_output(cmd,shell=True)
    return check_output

#random string genrator for salt
def random_string_generator(str_size):
    return ''.join(random.choice(string.ascii_letters) for x in range(str_size))


#genrate encryoted password
def crypt_password(password):
    salt_string = random_string_generator(16)
    crypted_password = crypt.crypt(password,salt_string)
    return crypted_password

#creating homr dir and copying from skel dir
def home_dir_create(username,home_dir):
    create_dir  = "mkdir -p " + home_dir
    command_exec(create_dir)
    copy_skel = "cp -rT /etc/skel " + home_dir
    command_exec(copy_skel)
    own_dir = "chown -R " + username + ":" + username + " "+ home_dir
    command_exec(own_dir)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    try:
        if request.method == 'POST':
            username = request.form['user']
            password = request.form['password']
            crypted_password = crypt_password(password)
            shell = request.form['shell']
            sudo_access = request.form['sudo']
            home_dir = request.form['home']
            if sudo_access == "yes":
                cmd = "adduser -d " +  home_dir +  " -p " + crypted_password  + " -s " + shell + " -G wheel "+ username
                command_exec(cmd)
            else:
                cmd = "adduser -d " +  home_dir +  " -p " + crypted_password  + " -s " + shell + " " + username
                command_exec(cmd)
            return "user successfully created."
    except:
        return "Something went wrong user not created!!!!!"
    return render_template('add.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_user():
    try:
        if request.method == 'POST':
            username = request.form['user']
            cmd = "userdel " + username
            command_exec(cmd)
            return "user successfully deleted"
    except:
        return "Something went wrong user not deleted!!!!!"
    return render_template('delete.html')

@app.route('/modify', methods=['GET', 'POST'])
def modify_user():
    try:
        if request.method == 'POST':
            username = request.form['user']
            select_value = request.form["selectedopt"]
            modify_value = request.form["modify"]
            if select_value == "password":
                cmd = 'echo ' + modify_value  + ' | passwd --stdin ' + username
                command_exec(cmd)
                return  "password changed"
            elif select_value == "shell":
                cmd = "usermod -s " + modify_value + " " + username
                command_exec(cmd)
                return  "shell changed"

            elif select_value == "homedir":
                home_dir_create(username,modify_value)
                return  "homedir changed"
            elif select_value == "sudo_access":
                cmd = "gpasswd -d " + username  + " wheel"
                command_exec(cmd)
                return "sudo access revoked"
    except:
        return "Something went wrong while modifying user!!!!!"
    return render_template('modify.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
