using Plots

@userplot StackedArea

# a simple "recipe" for Plots.jl to get stacked area plots
# usage: stackedarea(xvector, datamatrix, plotsoptions)
@recipe function f(pc::StackedArea)
    x, y = pc.args
    n = length(x)
    y = cumsum(y, dims=2)
    seriestype := :shape

    # create a filled polygon for each item
    for c=1:size(y,2)
        sx = vcat(x, reverse(x))
        sy = vcat(y[:,c], c==1 ? zeros(n) : reverse(y[:,c-1]))
        @series (sx, sy)
    end
end


"""
    eulerstep!(X, f, h; args=[])

Compute the next point in the solution of the differential equation using
Euler's method. The point is appended to ``X``.

# Arguments:
- `X` is an array of arrays containing the last known solution points.
- `f` is the right side in the differential equation U' = f(X).
- `h` is the step size.
"""
function eulerstep!(X::Vector{Vector{Float64}}, f::Function, h::Float64;
    args=[]::Array{Any})
    push!(X, X[end] + h * f(X,args...))
end

"""
    eulermethod(X0, f, h, stop; args=[])

Approximate the solution of a differential equation of the form
U'(x) = f(X)
U(x0) = X0
using Euler's method.

# Arguments
- `X0` is an initial point.
- `f` is the right side in the differential equation U' = f(X).
- `h` is the step size.
- `stop` is a function X -> Bool that determines when the method should
stop.
- `args` is an array of additional arguments to be passed to the 
derivative function
"""
function eulermethod(X0::Vector{Float64}, f::Function, h::Float64, 
    stop::Function; args=[]::Array{Any})
    X = [ X0 ]
    while !stop(X)
        eulerstep!(X, f, h, args=args)
    end
    return X
end

