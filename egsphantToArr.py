import numpy as np

class EgsPhantFile(object):

    def _load_egsphant(self, fName):
        data = open(fName).read().split('\n')
        mats = int(data[0])
        cur_line = 2 + mats
        x, y, z = map(int, data[cur_line].split())
        self.dims = (z, y, x)
        print(self.dims)
        cur_line = cur_line + 1
        x_coor, y_coor, z_coor = data[cur_line].split(), data[cur_line + 1].split(), data[cur_line + 2].split()
        self.coors = (z_coor, y_coor, x_coor)
        self.res = [(float(self.coors[i][-1]) - float(self.coors[i][0])) / self.dims[i] for i in range(3)]

        cur_line = cur_line + 3 + z * (y + 1)
        dens = []
        self.size = np.multiply.reduce(self.dims)
        while len(dens) < self.size:
            line_data = map(float, data[cur_line].split())
            dens += line_data
            cur_line += 1
        dens = list(filter(None, dens))
        self.dens = np.array(dens)
        self.dens = self.dens.reshape(self.dims)