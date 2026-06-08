import hashlib


def calculate_checksum(file_obj):

    sha256 = hashlib.sha256()
    total_size = 0
    file_obj.seek(0)

    while chunk := file_obj.read(8192):
        total_size += len(chunk)
        sha256.update(chunk)
    file_obj.seek(0)

    return (
        sha256.hexdigest(),
        total_size
    )