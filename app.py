import streamlit as st
from fractions import Fraction
from decimal import Decimal, getcontext

def gauss_seidel(A, b, initial_guess, decimal_places=5, mode='decimal'):
    n = len(A)
    x = initial_guess[:]

    if mode == 'decimal':
        getcontext().prec = decimal_places

    max_iterations = 100
    tolerance = 1e-10
    iter_count = 0
    error = tolerance + 1

    iteration_results = []

    while iter_count < max_iterations and error > tolerance:
        x_new = x[:]
        for i in range(n):
            sum_ax = sum(A[i][j] * x_new[j] for j in range(n) if j != i)
            if A[i][i] != 0:
                if mode == 'decimal':
                    x_new[i] = Decimal((b[i] - sum_ax) / A[i][i])
                elif mode == 'fraction':
                    x_new[i] = Fraction(b[i] - sum_ax, A[i][i])
        
        error = max(abs(x_new[i] - x[i]) for i in range(n))
        x = x_new[:]
        iter_count += 1


        # storing iterations results with error
        iteration_results.append((iter_count,x[:],float(error)))

    if iter_count == max_iterations:
        st.warning("Warning: Maximum iterations reached without convergence.")
    else:
        st.success(f"Converged to solution in {iter_count} iterations.")

    if mode == 'decimal':
        x = [round(float(x_i), decimal_places) for x_i in x]
    elif mode == 'fraction':
        x = [Fraction(x_i).limit_denominator() for x_i in x]

    return x , iteration_results

def main():
    st.title("Gauss-Seidel Iterative Method Solver")
    
    st.header("Matrix A")
    A_input = st.text_area("Enter matrix A (comma separated rows, newline for new row):", value="2,5\n1,7")
    
    st.header("Vector b")
    b_input = st.text_area("Enter vector b (comma separated values):", value="13,11")
    
    st.header("Initial Guess x")
    x_init_input = st.text_area("Enter initial guess for x (comma separated values):", value="0,0")
    
    decimal_places = st.number_input("Enter the number of decimal places for results:", value=5, min_value=1, max_value=15)
    
    mode = st.selectbox("Select mode for results:", ['decimal', 'fraction'])
    
    if st.button("Solve"):
        try:
            # Parsing matrix A
            A = []
            for row in A_input.split("\n"):
                A.append([int(num.strip()) for num in row.split(",")])

            # Parsing vector b
            b = [int(num.strip()) for num in b_input.split(",")]

            # Parsing initial guess
            x_init = [int(num.strip()) for num in x_init_input.split(",")]
            
            # Validating the inputs
            if len(A) != len(b):
                raise ValueError("The number of rows in A must be equal to the number of elements in b.")
            if len(x_init) != len(b):
                raise ValueError("The length of the initial guess must be equal to the number of elements in b.")

            # Solving the system
            solution, iteration_results = gauss_seidel(A, b, x_init, decimal_places, mode)
            st.write(f"Solution: {solution}")


            # displaying the iterations results
            st.header("Iteration Results")

            iteration_data = {
                "Iteration": [],
                "X": [],
                "Error": [],
            }

            
                

            for iter_count, x_values, error in iteration_results:
                if mode == 'fraction':
                    x_values_str = [f"{Fraction(val).limit_denominator().numerator}/{Fraction(val).limit_denominator().denominator}" for val in x_values]
                    
                else:
                    x_values_str = [round(float(x_i), decimal_places) for x_i in x_values]
                  
                    
                
                iteration_data["Iteration"].append(iter_count)
                iteration_data["X"].append(x_values_str)
                iteration_data["Error"].append(error if mode == 'decimal' else f"{Fraction(error).limit_denominator().numerator}/{Fraction(error).limit_denominator().denominator}")
            
            st.table(iteration_data)
        except ValueError as ve:
            st.error(f"Value Error: {ve}")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
