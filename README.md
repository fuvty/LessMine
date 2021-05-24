# LessMine

This is a python implementation of [LessMine: Reducing Sample Space and Data Access for Dense Pattern Mining](https://nicsefc.ee.tsinghua.edu.cn/media/publications/2020/HPEC20_321_XTdgG3v.pdf) 

> Fu T, Wan Z, Dai G, et al. LessMine: Reducing Sample Space and Data Access for Dense Pattern Mining[C]//2020 IEEE High Performance Extreme Computing Conference (HPEC). IEEE, 2020: 1-7.

NOTE: currently, the released python implementation is not the complete version because:

1. It only support clique mining now. However, the method can be applied to any dense pattern as defined in the paper. For further details, please refer to our paper ( e.g. Section VI. )
2. The optional *locality-aware partition* is not applied

## Problem setup

Given a query pattern Q and a target graph G, estimate how many Qs are there in G. For LessMine, the query pattern Q should be a dense pattern (the pattern that has at least one node connected to all other nodes).

Note that the number of Qs is defined as the *edge-induced subgraph* of G, a.k.a. *monomorphism* of G. 

## Core Idea

The essense of LessMine is `ConcurrentSample` and `UniformClose` . The function `LessMine_core` in `LessMine.py` provides a complete vision of how LessMine works. One can refer to the paper to understand how LessMine reduces the sample space and data access for dense pattern mining.

## Usage

The file `LessMine.py` provides the main user interface called `LessMine_main()` and the `main()` function is an example of how to use it

`LessMine_main` takes three args: `target`,  `query` and `num_estimator`

* `target_filename` is a string. It indicate the filename of the edge list of the target graph

* `query` is nx.Graph, the networkx instance of query. Note that for the nx.Graph instance with n nodes, the node set should be $\{0,1,\dots,n-1\}$, and the first node of any edge is always smaller than the second

* `num_estimator` is the number of estimators used to estimate the number of Q, one can adjust the number according to the time-error budget. Typically, larger G and Q requires more estimators.

  > We use 1E4 estimators on ego-Facebook(#E = 88234, #V = 4039) for 4-clique counting to get a approximately 10% error-bound



```
//  Created by Tianyu Fu on 2021/5/24.
//  Contributed by members of NICS Lab of Tsinghua University

//  Contact: futy18@mails.tsinghua.edu.cn
```

