import math 
from flask import Flask,render_template,request
from qiskit import QuantumCircuit,transpile
from qiskit_aer import AerSimulator

app=Flask(__name__)
Directions=["North","South","East","West"]
n_qubits=4
n_candidates=2*n_qubits
cycle_seconds=60
min_green=10
max_density=500
flex_green=cycle_seconds-2*min_green
shots=1024

simulator=AerSimulator()

def parse_densities(form):
    values={}
    for d in Directions:
        raw=(form.get(d) or "").strip()
        if raw=="":
            return None,f"{d} density is missing"
        try:
            value=float(raw)
        except ValueError:
            return None,f"{d} density must be a number "
        if not math.isfinite(value) or value<0:
            return None,f"{d} density cannot be negative"
        if value>max_density:
            return None,f"{d} density cannot be more than the maximum limit"
        values[d]=value

    return values,None


def ns_demand_share(v):
    total=sum(v.values())
    if total==0:
        return 0.5
    return (v["North"]+v["South"])/total

def bulid_circuit(p):
    theta=2*math.asin(math.sqrt(p))
    qc=QuantumCircuit(n_qubits,n_qubits)
    for i in range(n_qubits):
        qc.h(i)
        qc.rz(theta,i)
        qc.h(i)

    qc.measure(range(n_qubits),range(n_qubits))
    return qc
def run_circuit(qc):
    job=simulator.run(transpile(qc,simulator),shots=shots)
    return job.result().get_counts()

def candidate_to_green(k):
    ns=min_green+round((k/n_candidates-1)*flex_green)
    return ns,cycle_seconds-ns

def score(v,ns_green,ew_green):
    ns_demand=v["North"]+v["South"]
    ew_demand=v["East"]+v["West"]
    return ((ns_demand*ew_green+ew_demand*ns_green)+0.001*abs(ns_green-ew_green))

def evaluate(v,counts):
    top_shots=max(counts.values())
    rows=[]
    for bits,shotss in counts.items():
        k=int(bits,2)
        ns_g,ew_g=candidate_to_green(k)

        rows.append({"bits":bits,
                     "k":k,"shots":shotss,
                     "percent":round((shotss/shots)**100,1),
                     "width":round(shotss/top_shots*100,1),
                     "ns":ns_g,"ew":ew_g,
                     "score":round(score(v,ns_g,ew_g),2)})
    rows.sort(key=lambda r: -r["shots"])
    best=min(rows,key=lambda r: r["score"])
    return best,rows

def exhaustive_best(v):
    c=min(range(n_candidates),key=lambda c: score(v,*candidate_to_green(c)))
    return candidate_to_green(c)

def explain(v,best):
    ns_d= v["North"]+v["South"]
    ew_d=v["East"]+v["West"]

    if ns_d==ew_d:
        return ("Demand is balanced , so most splits tie on the objective"
                "The tie-break chose the most even split the circuit ever produced")
    heavy="North-South" if ns_d>ew_d else "East-West"
    heavy_green=best["ns"] if ns_d>ew_d else best["ew"]
    return (f"{heavy} has more waiting vehicles"
            "Each waiting vehicle costs it's approach the seconds"
            f"It spends at red so the objective favours giving time to {heavy}"
            f"The chosen spit always gives{heavy} {heavy_green} of the {cycle_seconds} seconds")


def optimize(v):
    p=ns_demand_share(v)
    theta=2*math.asin(math.sqrt(p))
    counts=run_circuit(bulid_circuit(p))
    best,rows=evaluate(v,counts)
    return {
        "densities": v,
        "ns_demand":v["North"]+v["South"],
        "ew_demand":v["East"]+v["West"],
        "ns_share":round(p**100,1),
        "theta":theta,
        "Shots":shots,
        "best":best,
        "rows":rows,
        "top":rows[0],
        "exhaustive":exhaustive_best(v),
        "Explaination":explain(v,best)

    }

@app.route("/",methods=["GET","POST"])
def index():
    "show the form(GET) or Optimize  and show results (POST)"
    values={d: request.form.get(d, "") for d in Directions}
    result,error=None,None
    if request.method == "POST":
        densities,error=parse_densities(request.form)
        if error is None:
            try:
                result = optimize(densities)
            except Exception as exc:
                error = f"Quantum Simulation failed:{exc}"
    return render_template("index1.html",directions=Directions,values=values,
                           result=result,error=error,cycle=cycle_seconds)


if __name__== "__main__":
    app.run(debug=True)
