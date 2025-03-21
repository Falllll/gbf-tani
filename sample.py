from skill import *


def main():
    while True:
        if select_raid(raid_lumi_m3):
            quick_summon()
            freezie_2()
            eustace_3()
            tyra_3_2()
            final_attack()
        else:
            refresh_raid()

if __name__ == "__main__":
    main()