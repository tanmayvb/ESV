from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain, TGraph, TMultiGraph, TGraphAsymmErrors, TMath, TH2D, TLorentzVector, TColor, AddressOf, gROOT, TNamed, gStyle, TF1, TLegend
from ROOT import kBlack, kBlue, kRed
import ROOT as ROOT
import os
import sys, optparse
from array import array
import math
import numpy as np
#import matplotlib.pyplot as plt


openf = TFile("Unfolded_Result_19UL18_Data_PY8.root", "read")
name = 'Unfold2D/Edd_TUnfold_NoReg_typ_0_eta0_3_pt7'
#openf = TFile("Total_unc.root","read")
#name = "total_erro_1_eta0_24_pt7"
hist1d=openf.Get(name)

bins = hist1d.GetNbinsX()

print ('Entries = ', hist1d.GetNbinsX())
def envnormal(hist1d):
	bins = hist1d.GetNbinsX()
	tot =[]
	for i in range(bins):
		tot.append(hist1d.GetBinContent(i+1))
		print(tot)

	xmin = [hist1d.GetXaxis().GetBinLowEdge(1)]
	xmax = [hist1d.GetXaxis().GetBinUpEdge(bins+1)]

	ymax =[max(tot)]
	ymin =[min(tot)]
	ymean = [sum(tot)/len(tot)]
	
	print (xmin, xmax, sum(tot), hist1d.GetEntries(), min(tot), max(tot))

def fit(hist1d,fitfun):
	ft = ROOT.TF1("ft",fitfun)
	hist1d.Fit(ft)
	return hist1d, ft

def plot(hist1,ft,hist2):
	c1 = TCanvas( 'c1', 'Example with Formula', 200, 10, 700, 500 )
	legend = TLegend(0.64, 0.62, 0.76, 0.92, "")
	legend.SetTextSize(0.030)
	legend.SetFillColor(0)
	#legend.SetFillStyle(3002)
	hist1.SetLineColor(0)
	ft.SetLineColor(2)
	hist1.SetLineColor(3)
	legend.SetBorderSize(0)
	legend.AddEntry(hist1,"Base Hist")
	legend.AddEntry(ft,"Fit Hist",'l')
	legend.AddEntry(hist2,"New Hist From Fit")
	hist1.Draw("p")
	ft.Draw("same")
	hist2.SetLineWidth(2)
	hist2.SetMarkerSize(0.4)
	hist2.SetMarkerStyle(21)
	hist2.Draw("same P")
	legend.Draw()
	c1.SaveAs("hunc.pdf")



	
#hist1d.Draw()
fithist, ft = fit(hist1d,"pol7")

fitresult = fithist.GetFunction("ft")
#print (fitresult.Eval(-2))

newhist1d = hist1d.Clone()
newhist1d.Reset()
for jbin in range(bins):
	xx = newhist1d.GetBinCenter(jbin+1)
	yy = fitresult.Eval(xx)
	newhist1d.SetBinContent(jbin+1,yy)
	print ("xx",xx,"  yy ",yy, " old Y =", hist1d.GetBinContent(jbin+1))

plot(hist1d, ft,newhist1d )

#newhist1d.SetLineColor(4)
#newhist1d.Draw("same")



#c1.SaveAs("hunc.pdf")
