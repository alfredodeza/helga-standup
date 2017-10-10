import random
import uuid
from helga.plugins import command
from helga import log

logger = log.getLogger(__name__)


bad_statuses = {
        'clueless': [
            (
                'I',
                '',
                'hrmn...',
            ),
            (
                "can't",
                "don't",
            ),
            (
                'recollect',
                'recall',
                'remember',
                'relate',
                'connect',
                'cite',
                'refer',
                'associate',
            ),
            (
                'yesterday',
                'anything',
                'this morning',
                'Friday',
            )
        ],
        'busy': [
            (
                'working',
                'blocked',
                'baffled',
                'puzzled',
                'frustrated',
                'flummoxed',
                'stupefied',
                'dumfounded',
                'befuddled',
                'terrified',
                'discombobulated',
                'vexed'
            ),
            (
                'on',
                'with',
                'at',
            ),
            (
                'issues',
                'tickets',
            ),
            (
                ', '.join([str(uuid.uuid4())[:8].upper() for i in range(random.randint(2, 5))]),
                ', '.join([str(uuid.uuid4())[:8].upper() for i in range(random.randint(2, 5))])
            )
        ],
        'literal': [
            (
                'I have a couple of questions about',
                'need to discuss more on the',
                'lets talk ',
                'we need to determine what is going on with the',
                'quick chat about',
            ),
            (
                'Riemann theorem',
                "Jacobi's elliptic functions",
                'Ahlfors theory',
                'Value distribution theory of holomorphic functions',
                'Hadamard three-circle theorem',
                'Bieberbach conjecture',
                "Landau's constants",
                "Schwarzian derivative",
            ),
        ]
    }



@command('standup',
         help='say a completely unacceptable thing for a standup status')
def standup(client, channel, nick, message, *args):
    key = random.choice(bad_statuses.keys())
    phrase = ''
    for item in bad_statuses[key]:
        phrase += random.choice(item) + ' '
    return phrase
