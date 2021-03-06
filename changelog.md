<Version 1.0> 03/21/2019
-Blueprints added and application has been split into 3 modular sub-systems:
--user authentication
--error
--core functions
-complete refactoring of routes, forms and application structure

<Version 0.9-b3> 02/05/2019
-[BUGFIX] pagination links fixed to point current page.
-secure password reset capability with email integration.
-timestamp improvements implemented with user posts and last sign in.
-user profile now only displays email and password fields if current user.
-button visual improvements in all forms.

<Version 0.9> 01/21/2019
-active state management for navbar links.
-various visual and layout improvements.
-[BUG] pagination links always redirect to index.
-changed route hierarchy for user accessibility. The default landing page is now 'explore.html'
-hide user social feed if not user is not authenticated.
-pagination features added to all pages that incorporate social feed.
-added logo in navbar.

<Version 0.8> 01/20/2019
-added follower and followed functionality.
-added pagination feature to templates.
-added tests.py allowing unit testing on User class model.
-pagination support for posts added.

<Version 0.7> 01/18/2019
-various visual improvements to home page and other templates.
-API call tweaked to get more relevant data.
-random_drink and category_drink methods to query API implemented.

<Version 0.6> 01/17/2019
-added support file requirements.txt listing flask packages required to run the application.

<Version 0.5> 01/16/2019
-logging errors to file.
-log critical errors and notify ADMINS via email
-user template now displays link to profile_editor on the current_user profile only.
-added support files changelog.txt and readme.txt

<Version 0.4> 01/15/2019
-added error handlers for error 404 and 500 to customized templates
-added profile_editor template giving USER ability to edit profile fields and make corresponding changes in database.
-[BUGFIX] profile_editor form invalidates form submission if new username requested already exists in database.
-

<Version 0.3> 01/14/2019
-added three new fields(headline, bio, last seen) in USER's profile template and corresponding USER table in database.
-added a signup template to register new users.
-added sub-template to render posts from database.

<Version 0.2> 01/12/2019
-SQL database initialized for testing.
-added two tables(users and posts).

<Version 0.1> 01/10/2019
-application initialized and basic file structure set up
-added a base template
-added a index template
-added a login template




Upcoming Features and Improvements:
-Integration of user and profile_editor templates making live updates possible.
-Error 500 will display improved template with 'brick wall' image.
-Error 404 will display template with 'cowboy' image.
