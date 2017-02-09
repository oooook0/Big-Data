from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
file = MPI.File.Open(comm, 'data-small.txt')
size = file.Get_size()
rank = comm.Get_rank()

num_process = comm.Get_size()
size_per_process = int(float(size) / num_process)
buffer_per_process = bytearray(size_per_process)
offset_per_process = rank * size_per_process

file.Iread_at(offset_per_process, buffer_per_process)
file.Close()
lines = buffer_per_process.decode().split('\r\n')[0:-1]
timestamps = [lines[0].split(',')[0], lines[-1].split(',')[0]]

print "%i|%s|%s|%i" % (rank, timestamps[0], timestamps[1], len(lines))


print len(timestamps)
