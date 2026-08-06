import tcurve

curve = tcurve.TCurve()

print(curve.set_acceleration(100.0))
print(curve.set_max_velocity(50.0))
print(curve.set_delta_phi(1000.0))


error, position = curve.get_point(0.5)

print(error)
print(position)

print(curve.get_tmax())
print(curve.get_curve_type())