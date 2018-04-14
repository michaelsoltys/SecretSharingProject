import re
from ThresTree import ThresTree
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
#import click
from fuzzyfinder import fuzzyfinder
from pygments.lexers.python import Python3Lexer


commands = {'add': ['Adds n child nodes to the specified node in the treeanization tree.',
					('add n k [#:#:#:...]\n'
								'\tn, is the number of children to make.'
								'k, is the number of keys from the children nodes that are needed to sign something.'
								'The last arguement is the address of the node the new nodes is being added to,'
								'if none is specified it is assumed the root is being added (if there isn\'t already).\n')],

			'split': ['No Description','No Usage Info'],

			'remove': ['Removes the specified node from the organization tree.',
						('remove #:#:#:...\n'
								'The last arguement is the address of the node that is being removed.\n')],

			'clear': ['No Description','No Usage Info'],

			'finalize': ['No Description','No Usage Info'],

			'display': ['No Description','No Usage Info'],

			'help': ['No Description','No Usage Info'],

			'quit': ['No Description','No Usage Info'],

			}

CommandCompleter = WordCompleter(list(commands.keys()),
                                    ignore_case=True)

class TreeMaker():
	"""docstring for TreeMaker"""
	def __init__(self):
		super(TreeMaker, self).__init__
		self.tree = ThresTree()

	def help(self, command=None):
		"""Prints help information.
		"""
		# If a command is given and it is in the commands dictionary, print the help info
		if command is not None and command in commands:
			print('------------------------------------------')
			print('{0} - {1[0]}\n\t{1[1]}\n'.format(command,commands[command]))
			print('------------------------------------------\n')
		else:
			# If the command didn't exist or none was given, print the help info for all commands
			for command_name in commands:
				print('------------------------------------------')
				print('{0} - {1[0]}\n\t{1[1]}\n'.format(command_name,commands[command_name]))
				print('------------------------------------------\n')


	def parse(self,command):
		command = command.lower()
		args = command.split(' ')

		# split n k #:#:#:...:#
		if args[0] == 'split':
			if len(args) > 1:
				if len(args) == 4 and re.match("[0-9]+ [0-9]+ ([0-9]+:?)+",command.split('split ')[1]):
					try:
						self.tree.search(args[-1]).split(int(args[1]),int(args[2]))
					except AssertionError as e:
						raise e
				else:
					raise AttributeError(command)

		# add #:#:...
		elif args[0] == 'add':
			if len(args) > 1:
				if len(args) == 2 and re.match("([0-9]+:?)+",command.split('add ')[1]):
					self.tree.addChild(args[-1])				
				else:
					raise AttributeError(command)

		# remove #:#:#:...:#
		elif args[0] == 'remove':
			if len(args) > 1:
				if len(args) == 2 and re.match("([0-9]+:?)+",command.split('remove ')[1]):
					self.tree.removeChild(args[-1])				
				else:
					raise AttributeError(command)
		
		# clear
		elif args[0] == 'clear':
			if len(args) > 1:
				pass #self.tree.clear()
			else:
				raise AttributeError(command)
		
		# finalize data
		elif args[0] == 'finalize':
			if len(args) == 2:
				self.tree.propagate(int(args[-1]))
			else:
				raise AttributeError(command)

		# display [--always,-a]
		elif args[0] == 'display':
			if len(args) > 1:
				if len(args) == 2 and re.match("(--always|-a)",args[1]):
					pass #self.tree.display(toggle=True)
				else:
					raise AttributeError(command)
			else:
				self.tree.display()
		
		# help [command]
		elif args[0] == 'help' or args[0] == 'h':
			if len(args) > 1:
				if len(args) == 2 and re.match("[a-zA-Z]+",args[1]):
					self.help(args[1])
				else:
					raise AttributeError(command)
			else:
				self.help()
		else:
			raise NameError(args[0])


	def repl(self):
		"""REPL function for tree maker. Loops until quit is called.
		"""

		while 1:
			try:
				user_input = prompt(u'>>>',
									# uses a history file
			                        history=FileHistory('history.txt'),
			                        # uses auto suggest from history functionality
			                        auto_suggest=AutoSuggestFromHistory(),
			                        # uses auto complete
			                        completer=CommandCompleter,
			                        # uses python3 syntax highlighting
			                        # this might be pointless
			                        lexer=Python3Lexer,
			                        )
				if user_input == 'q' or user_input == 'quit':
					break

				self.parse(user_input)

				# This allows for multiline intputs, but it also is kind of annoying if there is just one command
			    #click.echo_via_pager(user_input)

		    # 
			except NameError as e:
				print(e.args[0] + ': command not found.\nTry \'help\' or \'h\'.')
			except AttributeError as e:
				print(e.args[0] + ': invalid use.\nTry \'help [command]\' or \'h [command]\'.')
			except AssertionError as e:
				print(e.args[0])


if __name__ == '__main__':
	treeMaker = TreeMaker()
	treeMaker.repl()