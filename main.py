from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

def roam_simulator(T=50, initial_L=1000000, initial_N=1000, initial_Theta=500, A=1, R=10000, O=5000, O_prime=2000, alpha=0.5, beta=0.01, external_shock_time=None, external_shock_magnitude=0):
    L = [initial_L]
    N = [initial_N]
    Theta = [initial_Theta]
    V = [A * (initial_N**2) + (R - O + O_prime) * initial_N]
    p = [V[0] / L[0]]

    results = []

    for t in range(1, T+1):
        if external_shock_time and t == external_shock_time:
            N[-1] += external_shock_magnitude

        n_t = np.exp(-0.1 * t)  # Simplified n(t)
        L_t = L[-1] + n_t
        L.append(L_t)

        N_t = N[-1] + np.random.randint(0, 50)
        N.append(N_t)

        Theta_t = Theta[-1] + np.random.randint(0, 20)
        Theta.append(Theta_t)

        R_t = R + 100 * np.random.randn()
        O_t = O + 50 * np.random.randn()

        V_t = A * (N_t**2) + (R_t - O_t + O_prime) * N_t
        V.append(V_t)

        p_t = V_t / L_t
        p.append(p_t)

        results.append({
            "time": t,
            "tokens": L_t,
            "price": p_t,
            "networkValue": V_t,
            "miners": N_t,
            "validators": Theta_t
        })

    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    params = request.json
    results = roam_simulator(**params)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
