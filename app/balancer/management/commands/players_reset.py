from collections import Counter
from app.ladder.models import Player
from django.core.management.base import BaseCommand


PLAYERS = [
    ('Aarolus', 2500),
    ('Ariu', 5250),
    ('Bernrad', 2000),
    ('Bjocha', 6000),
    ('Broken Bonez', 1250),
    ('Captain Daddy', 1500),
    ('Chon', 5000),
    ('Clockwerk', 4250),
    ('Cory', 3500),
    ('Danreader', 3500),
    ('DasTone', 5000),
    ('DenDen', 5000),
    ('Divine.jpg', 4250),
    ('Eloquence', 4500),
    ('Emaggy', 4500),
    ('Eren', 4500),
    ('Everywherdo', 3500),
    ('Feggit', 5500),
    ('Frosty', 4250),
    ('frsm', 4000),
    ('Fy', 1500),
    ('Gibi', 4500),
    ('Hazza', 4000),
    ('Henry Bot', 3250),
    ('J1mmo', 4750),
    ('Jabo', 5250),
    ('Jullins', 3250),
    ('KaiserDMC', 1500),
    ('Keebo', 2750),
    ('Keiz', 4000),
    ('Khanzeal', 4000),
    ('Kilgannon', 5000),
    ('Kksweet Kieran', 4750),
    ('KoreanMadLetters', 5500),
    ('Krank', 4750),
    ('Kuhaku', 4250),
    ('Kyoto', 5250),
    ('L.Robilliard', 4250),
    ('Lazy Panda', 4000),
    ('Lees', 2500),
    ('Leyeon', 4000),
    ('Loryasas', 2500),
    ('Malalalez', 4500),
    ('Mamemolaredo', 4250),
    ('ManTheDan', 1000),
    ('MatyrDom', 2500),
    ('Maverick_2009', 3750),
    ('Medra', 3750),
    ('Mikel', 5000),
    ('Mitkoasd', 2500),
    ('MTD', 5500),
    ('Mtn', 6000),
    ('Muc1', 3750),
    ('Mystogan', 5500),
    ('Nahweh', 4500),
    ('Nathan', 3750),
    ('Nsphere', 5000),
    ('Nyk', 5000),
    ('OmN1m0n', 3000),
    ('Oscar', 5250),
    ('Owl', 2000),
    ('Panochita', 3000),
    ('Paradox', 2000),
    ('Polshy', 5750),
    ('Primal Soul', 3000),
    ('Procrastination', 4250),
    ('Pyranthos', 3750),
    ('RageZilla', 4750),
    ('Rawr', 4500),
    ('Razza215', 4000),
    ('RB', 3750),
    ('Roran', 4750),
    ('Rothwell', 5250),
    ('Sancitus', 3500),
    ('Sath', 4250),
    ('Sexysteve', 4000),
    ('SilverStorm', 3750),
    ('Ska', 3000),
    ('Skeliton', 1000),
    ('Skquad', 3750),
    ('SMMN', 5500),
    ('SoSkeptical', 4500),
    ('Spats Thalnor', 3000),
    ('SpiritBomb', 3750),
    ('sQuirtle', 4500),
    ('Supermoon', 4000),
    ('tenchitenkai', 1250),
    ('Tesla54', 4000),
    ('Texo Luck', 1500),
    ('TheIntCat', 2500),
    ('Tinie', 2500),
    ('tukatukera', 500),
    ('tuturu', 4500),
    ('Uvs', 3000),
    ('ven', 3250),
    ('Vision', 4000),
    ('Warrmie', 2500),
    ('Waterfalls', 5250),
    ('Whisky', 2500),
    ('Wifebeater', 5000),
    ('Wilko', 2500),
    ('Winter Blades', 3250),
    ('Wooo', 5500),
    ('xkcsh', 2500),
    ('Zanzebee', 3000),
    ('Zasa', 5500),
    ('Trollypops', 2500),
    ('Vaska', 5250),
    ('Rawr2', 1500),
    ('Smile', 5500),
    ('Paulvanpaks', 6000),
    ('Mura Masa', 6250),
    ('Woo', 5500),
    ('Valhalla', 3500),
    ('Marius', 6000),
    ('SgtAverage', 4750),
    ('920', 4500),
    ('T.O.P', 6500),
    ('JimDangle', 4000),
    ('Zap^', 4500),
    ('Tyskland', 4500),
    ('Crazy Duck', 3000),
    ('Laurix', 4500),
    ('SouL', 5000),
    ('TOP', 7000),
    ('AdrianJ', 2750),
    ('Shucs', 4250),
    ('Rosenkrantz', 3500),
    ('Potato', 5250),
    ('Helias', 5000),
]


class Command(BaseCommand):
    def handle(self, *args, **options):

        Player.objects.all().delete()

        for i, player in enumerate(PLAYERS):
            print 'Processing player: %d / %d' % (i, len(PLAYERS))

            Player(
                name=player[0],
                mmr=player[1],
                score=25
            ).save(calc_ranks=False)

        Player.objects.all().first().save()
