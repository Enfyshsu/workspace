import cmd
import logging
import sys

from pydnp3 import opendnp3

from outstation import OutstationApplication

stdout_stream = logging.StreamHandler(sys.stdout)
stdout_stream.setFormatter(logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'))

_log = logging.getLogger(__name__)
_log.addHandler(stdout_stream)
_log.setLevel(logging.DEBUG)

_log.disabled = True

class OutstationCmd(cmd.Cmd):
    """
        Create a pydnp3 DNP3Manager that acts as the Outstation in a DNP3 Master/Outstation interaction.
        Accept command-line input that sends simulated measurement changes to the Master,
        using the line-oriented command interpreter framework from the 'cmd' Python Standard Library.
    """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'outstation> '   # Used by the Cmd framework, displayed when issuing a command-line prompt.
        self.application = OutstationApplication()

    def startup(self):
        """Display the command-line interface's menu and issue a prompt."""
        print('Welcome to the outstation request command line. Supported commands include:')
        self.do_menu('')
        #self.cmdloop('Please enter a command.')
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.do_quit('')
        exit()

    def do_menu(self, line):
        """Display a menu of command-line options. Command syntax is: menu"""
        print('\ta\t\tAnalog measurement.\tEnter index and value as arguments.')
        print('\ta2\t\tAnalog 2 for MMDC.Vol (index 4).')
        print('\tb\t\tBinary measurement.\tEnter index and value as arguments.')
        print('\tb0\t\tBinary False for MMDC1.Amp.range (index 6).')
        print('\tc\t\tCounter measurement.\tEnter index and value as arguments.')
        print('\td\t\tDoubleBit DETERMINED_ON.\tEnter index as an argument.')
        print('\thelp\t\tDisplay command-line help.')
        print('\tmenu\t\tDisplay this menu.')
        print('\tquit')

    def do_quit(self, line):
        """Quit the command line interface. Command syntax is: quit"""
        self.application.shutdown()
        exit()


def main():
    cmd_interface = OutstationCmd()
    _log.debug('Initialization complete. In command loop.')
    cmd_interface.startup()
    _log.debug('Exiting.')


if __name__ == '__main__':
    main()
