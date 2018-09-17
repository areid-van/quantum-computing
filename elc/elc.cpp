#include <iostream>
#include <vector>
#include "ELC.h"

using namespace std;
using namespace ELCReduce;

ostream& operator<<(ostream& strm, const PBF<double>& obj){

  strm << "0 " << obj.cnst() << endl;

  for (PBF<double>::iterator it = obj.begin(); it != obj.end(); ++it)
  {
    size_t d = it.degree();
    strm << d;

    VVecIt vars = it.vars();
    for(size_t i=0; i<d; i++){
      strm << " " << *vars;
      vars++;
    }

    cout << " " << it.coef() << endl;
  }
  return strm;
}

int main(int, char**)
{
    int maxVar = -1;
    PBF<double> pbf;

    int mode;
    cin >> mode;
    
    while(!cin.eof())
    {
      int nvar;
      cin >> nvar;
      
      vector<int> vars(nvar);
      for(int i=0; i<nvar; i++){
          cin >> vars[i];
          maxVar = std::max(maxVar, vars[i]);
      }
      
      double coeff;
      cin >> coeff;

      switch(nvar){
          case 0:
              pbf.addConst(coeff);
              break;
          case 1:
              pbf.AddUnaryTerm(vars[0], 0, coeff);
              break;
          case 2:
              pbf.AddPairwiseTerm(vars[0], vars[1], 0, 0, 0, coeff);
              break;
          default:
              if(nvar > 4){
                  cerr << "Degree " << nvar << " terms not supported" << endl;
                  return 1;
              }
              int nperm = pow(2, nvar);
              vector<double> tmpVals(nperm, 0.);
              tmpVals[nperm-1] = coeff;
              pbf.AddHigherTerm(nvar, &vars[0], &tmpVals[0]);
      }

    }

    PBF<double> qpbf;
    if (mode == 0)
    {
        pbf.reduceHigher(); // Use the ELC technique to reduce higher-order terms without auxiliary variables
        pbf.toQuadratic(qpbf, maxVar+1); // Reduce the remaining higher-order terms using HOCR adding auxiliary variables
    }
    else if (mode == 1)
    {
        qpbf = pbf;
        qpbf.reduceHigherApprox(); // Use the approximate ELC technique to reduce higher-order terms without auxiliary variables
    }
    else if (mode == 2)
    {
        pbf.toQuadratic(qpbf, maxVar+1); // Reduce to Quadratic pseudo-Boolean function using HOCR.
    }

    cout << qpbf << endl;
    return 0;
}
