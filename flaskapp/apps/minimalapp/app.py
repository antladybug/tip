from flask_debugtoolbar import DebugToolbarExtension
from email_validator import validate_email, EmailNotValidError
from flask import Flask, render_template, request, url_for, redirect, flash
import logging

app = Flask(__name__)
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"

app.logger.setLevel( logging.DEBUG )
app.logger.critical( "fatal error" )
app.logger.warning( "warning" )
app.logger.info( "info" )
app.logger.debug( "debug" )
app.config[ "DRBUG_TB_INTERCEPT_REDIRECTS" ] = False
toolbar = DebugToolbarExtension( app )

@app.route( "/contact" )
def contact():
	return render_template ( "contact.html" )
	
@app.route( "/contact/complete", methods = [ "GET", "POST" ] )	
def contact_complete():
	if request.method == "POST":
		username = request.form[ "username" ]
		email = request.form [ "email" ]
		description = request.form [ "description" ]
		is_valid = True
		if not username:
			flash ( "ユーザ名は必須です" )
			is_valid = False
		if not email:
			flash ( "メールアドレスは必須です" )
			is_valid = False
		try:
			validate_email( email )
		except EmailNotValidError:
			flash ( "メールアドレスの形式で入力してください" )
			is_valid = False
		if not description:
			flash ( "問い合わせ内容は必須です" )
			is_valid = False
		if not is_valid:
			return redirect ( url_for ( "contact" ) )
		flash( "問い合わせ内容はメールにて送信しました。問い合わせありがとうございました。" )
		return redirect ( url_for ( "contact_complete" ) )
	return render_template ( "contact_complete.html" )

def create_app():
	# Flaskインスタンス生成
	app = Flask( __name__ )
	from apps.crud import views as crud_views
	app.register_blueprint( crud_views.crud, url_prefix = "/crud" )
	return app
