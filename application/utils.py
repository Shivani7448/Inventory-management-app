def grandTotal(list): #list of requests
  total = 0
  for req in list:
    if req.status == "approved":
      total += req.units_requested * req.product.cost
  return total

# req.product.cost > cost of product associated with this request