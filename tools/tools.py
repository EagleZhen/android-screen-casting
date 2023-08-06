import os
import sys

def print_separator(message="",line_size=30):
	left_line_size = (line_size-len(str(message)))//2
	right_line_size = line_size-left_line_size-len(str(message))
	print(f"{'='*left_line_size}{message}{'='*right_line_size}")

def print_message(*args):
	message = ' '.join(str(arg) for arg in args)
	print(message)

def pause(*args):
	print_message(*args)
	os.system("pause")

def stop(*args):
	print_message(*args)
	sys.exit()