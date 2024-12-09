import streamlit as st
import numpy as np
import time

class FastQuantumKeyDistribution:
    @staticmethod
    @st.cache_data
    def bb84_protocol(n_qubits=10, _seed=None):
        """
        Optimized BB84 Protocol Simulation with Detailed Outputs
        """
        if _seed is not None:
            np.random.seed(_seed)

        # Generate initial quantum state
        alice_bits = np.random.randint(2, size=n_qubits)
        alice_bases = np.random.randint(2, size=n_qubits)
        bob_bases = np.random.randint(2, size=n_qubits)

        # Photon polarizations based on bits and bases
        polarization_symbols = {
            (0, 0): '↑',  # 0 bit, + basis
            (0, 1): '↗',  # 0 bit, X basis
            (1, 0): '→',  # 1 bit, + basis
            (1, 1): '↘'   # 1 bit, X basis
        }

        # Derive polarizations
        alice_polarizations = [polarization_symbols[(bit, basis)] for bit, basis in zip(alice_bits, alice_bases)]

        # Simplified eavesdropping model
        def fast_eavesdropping_simulation(alice_bit, alice_basis):
            eve_intercept_prob = 0.2
            if np.random.random() < eve_intercept_prob:
                return np.random.randint(2)
            return None

        bob_results = []
        bob_polarizations = []
        eve_interventions = []
        matched_bases = []
        shared_key = []

        for bit, alice_basis, bob_basis, polarization in zip(alice_bits, alice_bases, bob_bases,alice_polarizations):
            eve_intervention = fast_eavesdropping_simulation(bit, alice_basis)
            eve_interventions.append(eve_intervention is not None)

            # Track matched bases
            if alice_basis == bob_basis:
                matched_bases.append(True)
                # Use original bit if no eavesdropping, else use eavesdropped bit
                bob_result = bit if eve_intervention is None else eve_intervention
                bob_results.append(bob_result)
                
                # Only add to shared key if bases match
                shared_key.append(bob_result)
                bob_polarizations.append(polarization)  # Bob measures the same polarization

            else:
                matched_bases.append(False)
                bob_results.append(np.random.randint(2))
                bob_polarizations.append('?' if bob_basis == 0 else '?')  # Bob can't measure correctly with mismatched basis

        # Faster error rate calculation
        comparison_subset = np.random.choice(n_qubits, n_qubits // 2, replace=False)
        error_rate = np.mean(alice_bits[comparison_subset] != np.array(bob_results)[comparison_subset])

        return {
            'alice_bits': alice_bits.tolist(),
            'bob_bits': bob_results,
            'alice_bases': ['+' if b == 0 else 'X' for b in alice_bases],
            'bob_bases':['+' if b == 0 else 'X' for b in bob_bases],
            'alice_polarizations': alice_polarizations,
            'bob_polarizations': bob_polarizations,
            'matched_bases': matched_bases,
            'shared_key': shared_key,
            'error_rate': error_rate,
            'eavesdropping_detected': error_rate > 0.15
        }

    @staticmethod
    @st.cache_data
    def e91_protocol(n_qubits=10, _seed=None):
        """
        Simplified E91 Protocol Simulation with Eavesdropping
        """
        if _seed is not None:
            np.random.seed(_seed)

        # Probabilistic entanglement and correlation simulation
        alice_bases = np.random.randint(2, size=n_qubits)
        bob_bases = np.random.randint(2, size=n_qubits)

        # Simulate correlated bits and potential eavesdropping
        correlated_bits = (alice_bases == bob_bases).astype(int)
        correlation_rate = np.mean(correlated_bits)

        # Simplified eavesdropping detection
        eavesdropping_detected = correlation_rate < 0.7

        return {
            'alice_bases': alice_bases.tolist(),
            'bob_bases': bob_bases.tolist(),
            'correlation_rate': correlation_rate,
            'eavesdropped': eavesdropping_detected
        }

def main():
    # Configure page with improved performance settings
    st.set_page_config(
        page_title="QKD Simulator", 
        page_icon="🔐", 
        layout="wide"
    )

    st.title("⚡ Quantum Key Distribution Simulator")

    # Sidebar for configuration
    st.sidebar.header("🔬 Simulation Parameters")
    
    protocol = st.sidebar.selectbox(
        "Select QKD Protocol",
        ["BB84 Protocol", "E91 Protocol"],
        help="Choose between two quantum key distribution protocols"
    )

    n_qubits = st.sidebar.slider(
        "Number of Qubits", 
        min_value=5, 
        max_value=50,  
        value=10,
        help="Adjust the number of qubits for key generation"
    )

    # Additional configuration options
    advanced_options = st.sidebar.expander("Advanced Options")
    with advanced_options:
        random_seed = st.number_input(
            "Random Seed", 
            min_value=0, 
            max_value=1000, 
            value=42,
            help="Set a seed for reproducible results"
        )

    # Performance monitoring and simulation
    if st.sidebar.button("🚀 Run Quantum Simulation", use_container_width=True):
        start_time = time.time()

        with st.spinner('Performing Quantum Simulation...'):
            if protocol == "BB84 Protocol":
                result = FastQuantumKeyDistribution.bb84_protocol(n_qubits, _seed=random_seed)
                
                # Results columns
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Qubits", n_qubits)
                with col2:
                    st.metric("Matched Bases", f"{sum(result['matched_bases'])} / {n_qubits}")
                with col3:
                    st.metric("Shared Key Length", len(result['shared_key']))
                with col4:
                    st.metric(
                        "Quantum Channel",
                        "Compromised" if result['eavesdropping_detected'] else "Secure"
                    )
            else:
                result = FastQuantumKeyDistribution.e91_protocol(n_qubits, _seed=random_seed)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Qubits", n_qubits)
                with col2:
                    st.metric("Correlation Rate", f"{result['correlation_rate']:.2%}")
                with col3:
                    st.metric(
                        "Quantum Channel",
                        "Compromised" if result['eavesdropped'] else "Secure"
                    )

            # Detailed data display
            st.header("Detailed Quantum Key Distribution Data")
            
            # Create tabs for different data views
            tab1, tab2, tab3 = st.tabs(["Bits & Bases", "Matched Bases", "Shared Key"])
            
            with tab1:
                if protocol == "BB84 Protocol":
                    st.subheader("Alice's Bits and Bases")
                    alice_data = {
                        'Bits': result['alice_bits'],
                        'Bases': result['alice_bases'],
                        'Polarizations Sent': result['alice_polarizations']
                    }
                    st.dataframe(alice_data)
                    
                    st.subheader("Bob's Bits and Bases")
                    bob_data = {
                        'Bits': result['bob_bits'],
                        'Bases': result['bob_bases'],
                        'Polarizations Measured': result['bob_polarizations']
                    }
                    st.dataframe(bob_data)
                else:
                    st.write("Detailed data is not available for the E91 protocol.")
            
            with tab2:
                if protocol == "BB84 Protocol":
                    st.subheader("Matched Bases Comparison")
                    matched_data = [
                        {
                            'Index': i, 
                            'Alice Basis': result['alice_bases'][i], 
                            'Bob Basis': result['bob_bases'][i], 
                            'Bases Matched': result['matched_bases'][i]
                        } for i in range(n_qubits)
                    ]
                    st.dataframe(matched_data, use_container_width=True)
                else:
                    st.write("Detailed data is not available for the E91 protocol.")
            
            with tab3:
                if protocol == "BB84 Protocol":
                    st.subheader("Shared Quantum Key")
                    st.write("Bits where Alice and Bob used the same basis:")
                    st.dataframe(result['shared_key'])
                else:
                    st.write("Detailed data is not available for the E91 protocol.")

            # Performance tracking
            end_time = time.time()
            st.sidebar.metric("Execution Time", f"{end_time - start_time:.2f} seconds")

    # Information section
    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 Quantum Key Distribution (QKD) simulates secure key exchange "
        "using quantum mechanical principles."
    )

if __name__ == "__main__":
    main()