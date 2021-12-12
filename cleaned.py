import re

def main():
	#read in targeted file to train
	with open('Ravens_weektest_2021.txt') as f:
		lines = f.readlines()
		clines = clean(lines)
		with open('testresult.txt', 'w') as c:
			for comment in clines:
				c.write(str(comment))

def clean(comments):

	cleaned_comments = []
	for i in range(len(comments)):

		remove_punctuation(comments[i])
		clean = ' '.join(re.sub("(/u/[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", comments[i]).split())
		if "deleted" in clean:
			clean = clean.replace("deleted", "")
		# words = clean.split()
		# # print(type(clean))
		# # print(clean)
		# # print(len(comments[i]))
		# if len(words) < 2:
		# 	clean = clean.replace(clean, "")
		clean = clean.lower()
		cleaned_comments.append(clean)
	cleaned_comments = '\n'.join(cleaned_comments)
	return cleaned_comments

def remove_punctuation(string):
	punctuation = '''!()-[]{};:'"\,<>/?@#$%^&*_~'''
	for punc in string:
		if punc in punctuation:
			string = string.replace(punc,"")
	return string



if __name__ == "__main__":
    main()
