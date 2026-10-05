---
id: 098
title: "NASA-ISRO Synthetic Aperture Radar (NISAR) mission and data products"
authors: "NASA (JPL) and ISRO; data distribution by NASA ASF DAAC (L-band) and ISRO Bhoonidhi (S-band)"
year: 2025
venue: "Satellite mission (launched 30 July 2025 on GSLV-F16 from Sriharikota); ASF NISAR data documentation"
link: https://nisar-docs.asf.alaska.edu/availability-overview/
code: none found (data products; open tools exist but not verified here)
category: upcoming
era: upcoming
tags: [sar, l-band, s-band, nasa, isro, india, mission, flood, agriculture, soil-moisture, open-data, hdf5]
verified: "2026-10-05 via https://nisar-docs.asf.alaska.edu/availability-overview/, https://nisar-docs.asf.alaska.edu/products-overview/, https://www.isro.gov.in/Mission_GSLVF16_NISAR_Home.html, https://www.earthdata.nasa.gov/data/platforms/space-based-platforms/nisar"
takeaway: "Free L-band and S-band SAR with a 12-day repeat, provisional calibrated products since July 2026 and S-band samples on ISRO Bhoonidhi; L-band sees flooding under crop canopy, an obvious next instrument for SatClip once access and format are wired in"
---

# NASA-ISRO Synthetic Aperture Radar (NISAR) mission and data products

## Problem
C-band SAR such as Sentinel-1 struggles under dense vegetation: flooded paddy, flooded forest and crop structure are hard to see because short wavelengths scatter off the canopy. There was no free, systematic, global L-band SAR mission, and India had no jointly owned dual-frequency radar mission.

## Approach
NISAR is a joint NASA-ISRO satellite carrying two SAR instruments: L-band (NASA) and S-band (ISRO). It uses a SweepSAR technique for a wide swath at fine resolution. Per ISRO: sun-synchronous orbit at about 747 km, 12-day global repeat, about 240 km swath, 5 to 100 m resolution, 5-year mission life, and a free and open data policy. ISRO lists crop extent, wetlands, biomass, glaciers and land deformation among applications.

## Data and benchmarks
Per the ASF documentation:
- Product levels: L0 raw (RRSD), L1 range-Doppler (RSLC, RIFG, ROFF, RUNW), L2 geocoded (GSLC, GOFF, GCOV, GUNW), L3 soil moisture (SME2). L2 and L3 are described as analysis-ready.
- Format: HDF5. GCOV (geocoded backscatter) pixel spacing 10, 20 or 80 m depending on range bandwidth.
- Beta products (released 27 February 2026): over 100,000 pre-calibration L1 to L3 products from 17 October 2025 to 20 January 2026.
- Provisional products (released 20 July 2026): calibrated and partially validated, with known ionospheric issues at higher latitudes. A reprocessing campaign toward validated versions is planned for Q4 2026.
- Latency: L0B 2 to 10 hours; L1 to L3 about 36 to 72 hours.
- L-band via ASF DAAC (Vertex / Earthdata search); a limited set of S-band sample products (RSLC, GSLC, GCOV from January to February 2026) via ISRO's Bhoonidhi hub.
- A permanent instrument data gap from 27 July to 10 August 2026 is noted.

## Key results
No benchmark results apply; this is a mission. Its significance is availability: free dual-frequency SAR over India on a regular schedule.

## Limitations
- Products are HDF5, not Cloud-Optimized GeoTIFF, and we did not confirm a public STAC catalog; reading small windows remotely needs extra tooling.
- Provisional calibration only; validated products are still pending as of this entry.
- S-band access for the public appears limited to samples so far.
- 12-day repeat is slower than the combined Sentinel-1 constellation (entry 100) for fast-moving floods.
- Earthdata login is required for ASF downloads (standard NASA practice; not re-checked here).

## What it means for SatClip
- Not a threat; an opportunity, and strong India relevance for the SIH pitch (an ISRO co-built mission).
- Adopt, in phase 2: add an L-band GCOV water and flooded-vegetation instrument for monsoon paddy districts, where Sentinel-1 C-band under-detects floodwater under canopy. Keep it as a separate, labelled instrument on the evidence card with its own calibration.
- Engineering: write a small HDF5 subsetting reader, or convert GCOV tiles to COG per district, and record NISAR granule IDs and product version (beta, provisional, validated) in the receipt. Abstain or reduce confidence on beta products.
- Use the SME2 soil moisture product as context for crop-condition answers once validated.
- Pitch line: SatClip is designed to plug in Indian national assets (NISAR via Bhoonidhi, NRSC flood products) as they become available, not just European data.
