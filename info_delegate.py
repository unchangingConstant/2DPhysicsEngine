from simulations import Simulation

"""
Note: How do you edit sims? Easy, you fetch it, edit it, then add it back to the database
with the same tag, where it'll replace the old sim.
"""

class InfoDelegate():

    def __init__(file_path: str):
        pass

    def fetch_sim(sim_name: str) -> Simulation:
        pass

    def add_sim(sim: Simulation):
        pass
    