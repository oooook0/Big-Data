import time
import psutil
import argparse
import logging
from mpi4py import MPI


def seperate_data(buffer_per_process):

    signal, noise = [], []
    dateSet = {}
    # garbage = []

    buff_decode = buffer_per_process.decode().split('\n')[:-1]

    for i, line_to_select in enumerate(buff_decode):

        tmp = line_to_select.split(',')

        # deal with broken line
        if len(tmp) != 3:
            # garbage.append(line_to_select)
            pass
        # remove the invalid data
        elif 'o' in tmp[0] or 'O' in tmp[0]:
            noise.append(tmp)
        # remove the data whose price or volum less or equal than 0
        elif tmp[1][0] == '-' or tmp[2][0] == '-' or tmp[1][0] == '0' or tmp[2][0] == '0':
            noise.append( tmp)
        else:
            signal.append(tmp)
            if tmp[0][:8] not in dateSet:
                dateSet[tmp[0][:8]] = 1
            else:
                dateSet[tmp[0][:8]] += 1

    # this is mainly for finding abnormally large price compared to the prevous time slot
    signal.sort()

    # remove those date whoes percentage is less than 1%
    dateRemove = []
    for k, v in dateSet.iteritems():
        if v / float(len(buff_decode))  < 0.01:
            dateRemove.append(k)
    # confirm that the date is not the latest date
    for date in dateRemove:
        if date == max(dateSet):
            dateRemove.remove(date)

    for i, line_to_select in enumerate(signal):
        if line_to_select[0][:8] in dateRemove:
            noise.append(line_to_select)
            del signal[i]
        elif i > 0:
            # remove the duplicated data
            if line_to_select[0] == signal[i-1][0]:
                noise.append(line_to_select)
                del signal[i]
            # remove abnormal large price
            elif abs(len(tmp[1]) - len(signal[-1][1])) > 1:
                noise.append(line_to_select)
                del signal[i]

    # noise.sort()

    signal_data = '\n'.join([','.join(i) for i in signal]) + '\n'
    noise_data = '\n'.join([','.join(i) for i in noise]) + '\n'

    return signal_data,noise_data


if __name__ == "__main__":

    # time tracker
    start = time.time()
    i_time, process_time, o_time = 0, 0, 0

    # passing the parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-file", help="Enter the file name", required=True)
    args = parser.parse_args()

    # initial MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # adding log file
    if rank == 0:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='scrub.log',
                            filemode='w')
        logging.info("initializing MPI...")


    in_file = MPI.File.Open(comm, args.file, MPI.MODE_RDONLY, MPI.INFO_NULL)
    # in_file = MPI.File.Open(comm, "data-big.txt", MPI.MODE_RDONLY, MPI.INFO_NULL)

    if rank == 0:
        logging.info("open the input file %s" % rank)

    file_size = in_file.Get_size()
    num_process = comm.Get_size()

    read_size = file_size if file_size < (psutil.virtual_memory().free) / 70 else (psutil.virtual_memory().free) / 70
    size_per_process = int(float(read_size) / num_process)

    iteration = float(file_size) / read_size

    buffer_per_process = bytearray(size_per_process)

    out_file0 = MPI.File.Open(comm, "noise.txt", MPI.MODE_WRONLY | MPI.MODE_CREATE)
    out_file1 = MPI.File.Open(comm, "signal.txt", MPI.MODE_WRONLY | MPI.MODE_CREATE)

    if rank == 0:
        logging.info("file size = %s, read size = %s, size per process = %s" % (file_size, read_size, size_per_process))
        logging.info("iteration = %s" % iteration)

    counter = 0

    while counter < iteration:

        if rank == 0:
            logging.info("-- %s / %i --" % (counter, iteration))

        # read the data
        i_time_start = time.time()

        if counter * read_size + rank * size_per_process + size_per_process <= file_size:
            in_file.Read_at(counter * read_size + rank * size_per_process, buffer_per_process)
        elif counter * read_size + rank * size_per_process > file_size:
            buffer_per_process = bytearray(0)
            in_file.Read_at(counter * read_size + rank * size_per_process, buffer_per_process)
        else:
            buffer_per_process = bytearray(file_size - counter * read_size - rank * size_per_process)
            in_file.Read_at(counter * read_size + rank * size_per_process, buffer_per_process)

        i_time_end = time.time()
        i_time += (i_time_end -i_time_start)

        counter += 1

        if rank == 0:
            logging.info("counter %s in iteration %s done on reading" % (counter, iteration))
            logging.info("starting to process the data")

        '''process the data
           1. deal with broken lines
           2. seperate the noise and signal
        '''
        process_time_start = time.time()

        # seperate the data
        signal_data, noise_data = seperate_data(buffer_per_process)

        process_time_end = time.time()
        process_time += (process_time_end - process_time_start)

        # output the data
        o_time_start = time.time()

        if rank == 0:
            logging.info("processing the data is done")
            logging.info("starting to output...")

        out_file0.Write_ordered(noise_data.encode(encoding='UTF-8'))
        out_file1.Write_ordered(signal_data.encode(encoding='UTF-8'))

        o_time_end = time.time()
        o_time += (o_time_end - o_time_start)


    in_file.Close()
    out_file0.Close()
    out_file1.Close()
    comm.Barrier()
    end = time.time()

    if rank == 0:
        print "Total time of input: {} seconds".format(str(i_time))
        print "Total time of processing data: {} seconds".format(str(process_time))
        print "Total time of output: {} seconds".format(str(o_time))
        print "Total time of the whole program: {} seconds".format(str(end - start))
        logging.info("total input time %s seconds; total output time %s seconds; total processing time %s seconds" % (i_time, o_time,process_time))
        logging.info("total run timem %s seconds" % str(end - start))
        logging.info("program ended")
