TISSUE_DESCRIPTIONS = {
    "cardiac": (
        "Cardiac action potentials have a characteristic long plateau phase (Phase 2) 
        "that lasts 200-300ms. This extended depolarization is due to slow Ca²⁺ channels 
        "and prevents tetanic contractions, ensuring proper heart pumping function. 
        "The five phases are: 0 (rapid depolarization), 1 (early repolarization), 
        "2 (plateau), 3 (repolarization), and 4 (resting potential)."
    ),
    "neuron": (
        "Neuronal action potentials are rapid, lasting only 1-2ms. They feature a sharp 
        "depolarization phase followed by quick repolarization and a brief hyperpolarization 
        "period. This rapid signaling allows neurons to transmit information quickly along 
        "axons. The brief refractory period enables high-frequency firing."
    ),
    "skeletal": (
        "Skeletal muscle action potentials have an intermediate duration of 2-5ms. 
        "They are similar to neuronal action potentials but slightly longer. The action 
        "potential propagates along the muscle fiber membrane (sarcolemma) and into 
        "T-tubules, triggering calcium release and muscle contraction."
    )
}

HR_RANGES = {
    "resting": (60, 80),
    "exercise": (120, 150),
    "stress": (90, 110),
    "sleep": (40, 60)
}