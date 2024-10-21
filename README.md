Welcome to the personas population project,

The main program for this study is the 'current' folder; methodologies used to discover what was needed of it are in 'preliminary'.

Once you are in the current folder, the program resembles this architecture:

Human data cleaning folder:
  We needed human data to learn the subdemographic requirements of our population and compute similarity from lm to human.
  With the cleaning.py file, we add instructions to download the human data and a battery of questions from the human survey to generate personas and responses.
  
Personas.py:
  Generating all personas and collecting their responses based on the cleaned population data and battery from the human data cleaning folder

Results folder:
  Contains csv's, one for each population - human, union-llm, political-llm, intersectional-llm, containing all of their responses to the questions in our selected battery.
  There is an unused but kept csv named intersect-og, which is what the intersectional approach generated, with error of responding with a string. The causation of error was not found, and the personas.py program was not rerun to generate new results. The intersectional csv used in analysis has a breif update at the error, line 692, to turn the string "2\n" into an integer, 2, without the new line

Wasserstein-distance.py
  Computes the distance metric on each question's responses with SciPy's wasserstein distance module
