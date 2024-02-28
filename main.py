import os

curdir = os.getcwd()
scf_dir = os.path.join(curdir, "scf.in")
read_scf = open(scf_dir, "r")
scf_lines = read_scf.readlines()
all_disp_objs = []
displacement_factor = 0.3

class Displacement:
    def __init__(self, displacemts_array):
        self.disp_arr = displacemts_array
    def create_displaced_cell(self):
        global my_cell
        displaced_cell = my_cell
        atom_index = 0
        for atom in displaced_cell.atoms:
            displacements_vecs = self.disp_arr[atom_index]
            xvec = displacements_vecs[0] * displacement_factor
            yvec = displacements_vecs[1] * displacement_factor
            zvec = displacements_vecs[2] * displacement_factor
            atom.displace(xvec, yvec, zvec)
            atom_index += 1
        displaced_cell.introduce_in_frac()




class Cell:
    def __init__(self, xdim, ydim, zdim):
        self.xdim = xdim
        self.ydim = ydim
        self.zdim = zdim
        self.atoms = []
    def introduce_in_angstroms(self):
        for atom in self.atoms:
            x = atom.x_ang
            y = atom.y_ang
            z = atom.z_ang
            print("{}\t{}\t{}\t{}".format(atom.element, x, y, z))
    def introduce_in_frac(self):
        for atom in self.atoms:
            x_frac = atom.x_ang / self.xdim
            y_frac = atom.y_ang / self.ydim
            z_frac = atom.z_ang / self.zdim
            print("{}\t{}\t{}\t{}".format(atom.element, x_frac, y_frac, z_frac))

class Atom:
    def __init__(self,element, x_ang, y_ang, z_ang):
        self.element = element
        self.x_ang = float(x_ang)
        self.y_ang = float(y_ang)
        self.z_ang = float(z_ang)
    def displace(self, x_vec, y_vec, z_vec):
        self.x_ang += x_vec
        self.y_ang += y_vec
        self.z_ang += z_vec
        if self.x_ang < 0:
            self.x_ang += x_dim
        if self.y_ang < 0:
            self.y_ang += y_dim
        if self.z_ang < 0:
            self.z_ang += z_dim

for i in range(0, len(scf_lines)):
    line = scf_lines[i]
    if "CELL_PARAMETERS" in line:
        x_dim = float(scf_lines[i+1].split()[0])
        y_dim = float(scf_lines[i+2].split()[1])
        z_dim = float(scf_lines[i+3].split()[2])
    if "ATOMIC_POSITIONS" in line:
        start_atoms_index = i+1
        break

my_cell = Cell(x_dim, y_dim, z_dim)

for i in range(start_atoms_index, len(scf_lines)):
    line = scf_lines[i]
    cutted = line.split()
    if len(cutted) > 3:
        x_coord = float(cutted[1]) * x_dim
        y_coord = float(cutted[2]) * y_dim
        z_coord = float(cutted[3]) * z_dim
        symbol = cutted[0]
        new_atom = Atom(symbol, x_coord, y_coord, z_coord)
        my_cell.atoms.append(new_atom)

my_cell.introduce_in_angstroms()
my_cell.introduce_in_frac()
disp_dir = os.path.join(curdir, "disp.modes")
r_disp = open(disp_dir, "r")
disp_lines = r_disp.readlines()
all_disps = []
new_disp = []
for i in range(0, len(disp_lines)):
    line = disp_lines[i]
    #print(line)
    if "freq" in line or line.strip() == "":
        print(new_disp)
        if len(new_disp) > 0:
            all_disps.append(new_disp)
        new_disp = []
    else:
        xvec = float(line.split()[1])
        yvec = float(line.split()[3])
        zvec = float(line.split()[5])
        disp_to_add = [xvec, yvec, zvec]
        new_disp.append(disp_to_add)

displacement_index = 0
for mode in all_disps:
    #print("Tworze komórkę numer {}.".format(displacement_index))
    print("\n")
    new_displacemt = Displacement(mode)
    new_displacemt.create_displaced_cell()
    displacement_index += 1
