rem  # This is a comment.
rem  # The first code line is to run the script with minimised command prompt
rem  # It sets a flag then runs another instance of itself but minimised and exits when run the first time
rem  # When it runs the second time, the flag is set and therefore the python script runs.

if not DEFINED IS_MINIMISED set IS_MINIMISED=1 && start "" /min "D:\Users\Charles Turvey\Documents\Python\Projects\Glitcheroony\Glitch.bat" && exit
python "D:\Users\Charles Turvey\Documents\Python\Projects\Glitcheroony\Glitcheroony.py"
