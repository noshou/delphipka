// SPDX-License-Identifier: LGPL-3.0-or-later
// Modified on branch nucleic-acids by noshou: new file.

//
// Reuse of the products of CDelphiSpace::setGaussian(). The charged and the neutral state of a titratable site are
// solved on the same grids around the same atoms and differ only in a few charges, which setGaussian() never reads,
// so its dielectric maps and boundary-point list are identical and the second state can take them from here.
// An entry is only used when every input of setGaussian() is bitwise equal (the key below), so a hit changes nothing.
//   BAYSOL_GAUSS_CACHE=0        switches the cache off
//   BAYSOL_GAUSS_CACHE_CHECK=1  on a hit also recomputes and aborts if the restored state differs (test aid)
#ifndef BAYSOL_GAUSS_CACHE_H_
#define BAYSOL_GAUSS_CACHE_H_

#include <cstddef>
#include <deque>
#include <string>
#include <vector>

#include "../interface/environment.h"
#include "../misc/misc_grid.h"

const size_t GAUSS_CACHE_ENTRIES     = 4;                    // one site's four solves (base, two focusings, residue alone)
const size_t GAUSS_CACHE_ENTRY_BYTES = 96ul*1024*1024;       // larger states are not kept: for a 175^3 grid (265 MB) copying
                                                             // them in and out costs more than setGaussian() and, with several
                                                             // ranks, the memory makes the whole run slower (3HDD: 4 ranks
                                                             // 252 s with the cache, 135 s without)
const size_t GAUSS_CACHE_BYTES       = 256ul*1024*1024;      // upper bound on what is kept per process

struct GaussState
{
    std::vector< SGrid<delphi_real> > g1, g2;           // gepsmp, gepsmp2 over indices 0..iGrid
    std::vector<char> deb;                              // idebmap over indices 0..iGrid
    std::vector< SGrid<delphi_integer> > ibgrd;         // boundary points
    delphi_integer ibound;                              // iBoundNum

    size_t bytes() const
    {
        return (g1.size() + g2.size())*sizeof(SGrid<delphi_real>) + deb.size() + ibgrd.size()*sizeof(SGrid<delphi_integer>);
    }
};

class GaussCache
{
public:
    struct Entry { std::string key; GaussState state; };

    static GaussCache& instance() { static GaussCache c; return c; }

    const GaussState* find(const std::string& key) const
    {
        for (const Entry& e : entries) if (e.key == key) return &e.state;
        return NULL;
    }

    void store(const std::string& key, GaussState& state)
    {
        if (state.bytes() > GAUSS_CACHE_ENTRY_BYTES) return;
        entries.push_back(Entry());
        entries.back().key = key;
        entries.back().state.g1.swap(state.g1);  entries.back().state.g2.swap(state.g2);
        entries.back().state.deb.swap(state.deb); entries.back().state.ibgrd.swap(state.ibgrd);
        entries.back().state.ibound = state.ibound;
        size_t total = 0;
        for (const Entry& e : entries) total += e.state.bytes();
        while (!entries.empty() && (entries.size() > GAUSS_CACHE_ENTRIES || total > GAUSS_CACHE_BYTES))
        {
            total -= entries.front().state.bytes();
            entries.pop_front();
        }
    }

    template <class T> static void add(std::string& key, const T& v) { key.append(reinterpret_cast<const char*>(&v), sizeof(T)); }

private:
    std::deque<Entry> entries;
};

#endif
