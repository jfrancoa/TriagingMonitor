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
import bugzilla
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import urllib

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
        self.dfg = ""
        self.bz_url = "https://bugzilla.redhat.com"
        self.bzapi = bugzilla.Bugzilla(self.bz_url)
        self.str_query = "/buglist.cgi?GoAheadAndLogIn=Log%20in&action=wrap&bug_status=NEW&bug_status=ASSIGNED&bug_status=POST&bug_status=MODIFIED&bug_status=ON_DEV&bug_status=ON_QA&bug_status=VERIFIED&bug_status=RELEASE_PENDING&chfield=%5BBug%20creation%5D&chfieldto=Now&f1=cf_internal_whiteboard&f10=cf_qe_conditional_nak&f11=CP&f13=CP&f14=cf_internal_whiteboard&f2=component&f3=OP&f4=priority&f5=bug_severity&f6=flagtypes.name&f7=OP&f8=keywords&f9=cf_conditional_nak&j7=OR&keywords=FutureFeature%2C%20Tracking%2C%20Documentation%2C%20&keywords_type=nowords&list_id=9067676&n3=1&o1=substring&o10=isnotempty&o14=substring&o2=notsubstring&o4=notequals&o5=notequals&o6=anywordssubstr&o8=substring&o9=isnotempty&order=opendate%20DESC%2Cchangeddate%20DESC%2Cassigned_to%2Cbug_id%20DESC&query_format=advanced&v1=DFG%3A&v14={0}&v2=doc&v4=unspecified&v5=unspecified&v6=rhos%20rhel&v8=Triaged"

        try:
           if not self.bzapi.logged_in:
            self.bzapi.interactive_login()

        except:
            self.bzapi.interactive_login()

    def _get_untriage_bugs(self):

        query = self.bzapi.url_to_query(self.bz_url+self.str_query.format(urllib.quote(self.dfg)))
        return self.bzapi.query(query)

    def untriage(self, irc, msg, args):
        """takes no arguments

         Returns the number of untriaged Bugzillas for the DFG.
         """

        if not self.dfg:
            irc.reply("Use 'configure' command to specify the"
                      "DFG for this channel")
            return
       
        bugs = self._get_untriage_bugs()
        irc.reply(str(len(bugs)) + " untriaged bugs for " + str(self.dfg))

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

        irc.reply(msg.args)

    configure = wrap(configure, ['text'])

    def checkdfg(self, irc, msg, args):
        """ takes no arguments

        Returns the dfg configured for this channel used
        to query the number of untriaged BZs.
        """

        if self.dfg:
            irc.reply(self.dfg)
        else:
            irc.reply("Use 'configure' command to specify the "
                      "DFG for this channel")

    checkdfg = wrap(checkdfg)

    def which(self, irc, msg, args):
        """takes no arguments

         Returns the list of untriaged Bugzillas for the DFG.
         """

        if not self.dfg:
            irc.reply("Use 'configure' command to specify the"
                      "DFG for this channel")
            return
       
        bugs = self._get_untriage_bugs()
        for bug in bugs:
            irc.reply("BZ " + str(bug.id) + ": " + str(bug.summary))

    which = wrap(which)

Class = TriagingMonitor


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
