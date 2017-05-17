from hitori.player import HitoriPlayer

if __name__ == "__main__":
    player = HitoriPlayer()
    for _ in range(10):
        player.play()
        player.play_again()
