###
# Copyright (c) 2018, Jose Luis Franco Arza
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('TriagingMonitor')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class TriagingMonitor(callbacks.Plugin):
    """This plugin provides a set of commands to make the Triaging duty
    much simpler and help keeping the number of untriaged bugs at its
    lowest. The plugin will retrieve the number of untriaged Bugzillas
    upon request or it can be programmed to do it everyday at the same
    time."""
    
    def __init__(self, irc):
        self.__parent = super(TriagingMonitor, self)
        self.__parent.__init__(irc)
        self.dfg = "DFG:Upgrades"

    def untriage(self, irc, msg, args):
        """takes no arguments

         Returns the number of untriaged Bugzillas for the DFG.
         """
        irc.reply(str(0))

    untriage = wrap(untriage)

    def configure(self, irc, msg, args, dfg):
        """<dfg>

        Modifies the untriaged query for any specific DFG. By
        default is set to 'DFG:Upgrades'.
        """
        if "DFG:" not in dfg:
            irc.reply("You need to specify the DFG as DFG:<name>"
                      "e.g DFG:Upgrades")
        else:
            self.dfg = str(dfg)
            irc.replySuccess()
    
    configure = wrap(configure, ['string'])

Class = TriagingMonitor


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
