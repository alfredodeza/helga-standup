import random
import uuid
from helga.plugins import command
from helga.db import db
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
    arguments = args[1]
    if not arguments:
        # make a phrase
        phrases = []
        key = random.choice(bad_statuses.keys())
        phrase = ''
        for item in bad_statuses[key]:
            phrase += random.choice(item) + ' '

        phrases.append(phrase)

        count = db.standup.count()
        if count:
            status = db.standup.find()[random.randrange(count)]
            phrases.append(status['msg'])

        client.msg(channel, random.choice(phrases))

    else:
        cmd = arguments.pop(0)
        message = ' '.join(arguments)
        if not message:
            return 'I need an actual phrase to add or remove'
        if cmd == 'add':
            db.standup.update_one({
                'msg': message,
            }, {'$set': {'msg': message}}, upsert=True)

        if cmd == 'remove':
            status_to_forget = message

            logger.debug('will attempt to purge: {}'.format(status_to_forget))

            remove_result = db.standup.delete_one({
                'msg': status_to_forget,
            })

            logger.debug('remove_result: {}'.format(remove_result.deleted_count))

            if remove_result.deleted_count == 1:
                return 'done.'
            else:
                return 'not found :('
