from maintenance.models import Piece


def get_pieces():
    return Piece.objects.all()


def get_pieces_machine(machine_id):
    return Piece.objects.filter(machine_id=machine_id)