# used for CVS snapshots:
%define CVSDATE %{nil}
%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%define WITH_SELINUX 1
%endif
%define desktop_file 0
%if %{desktop_file}
%define desktop_file_utils_version 0.2.93
%endif

%define withnetbeans 1

%define withvimspell 0
%define withhunspell 0
%define withruby 1

%define baseversion 7.4
#used for pre-releases:
%define beta %{nil}
%define vimdir vim74%{?beta}
%define patchlevel 389

Summary: The VIM editor
URL:     http://www.vim.org/
Name: vim
Version: %{baseversion}.%{beta}%{patchlevel}
Release: 2%{?dist}
License: Vim
Group: Applications/Editors
Source0: ftp://ftp.vim.org/pub/vim/unix/vim-%{baseversion}%{?beta}%{?CVSDATE}.tar.bz2
Source3: gvim.desktop
Source4: vimrc
Source5: virc
#Source5: ftp://ftp.vim.org/pub/vim/patches/README.patches
Source7: gvim16.png
Source8: gvim32.png
Source9: gvim48.png
Source10: gvim64.png
Source11: Changelog.rpm
Source12: vi_help.txt
%if %{withvimspell}
Source13: vim-spell-files.tar.bz2
%endif
Source14: spec-template

Source24: vimfiles.tar.gz

%if %{withhunspell}
BuildRequires: hunspell-devel
%endif
# Patches 001 < 999 are patches from the base maintainer.
# If you're as lazy as me, generate the list using
# for i in `seq 1 52`; do printf "Patch%03d: http://ftp.vim.org/pub/vim/patches/7.4/7.4.%03d\n" $i $i; done
Patch001: http://ftp.vim.org/pub/vim/patches/7.4/7.4.001
Patch002: http://ftp.vim.org/pub/vim/patches/7.4/7.4.002
Patch003: http://ftp.vim.org/pub/vim/patches/7.4/7.4.003
Patch004: http://ftp.vim.org/pub/vim/patches/7.4/7.4.004
Patch005: http://ftp.vim.org/pub/vim/patches/7.4/7.4.005
Patch006: http://ftp.vim.org/pub/vim/patches/7.4/7.4.006
Patch007: http://ftp.vim.org/pub/vim/patches/7.4/7.4.007
Patch008: http://ftp.vim.org/pub/vim/patches/7.4/7.4.008
Patch009: http://ftp.vim.org/pub/vim/patches/7.4/7.4.009
Patch010: http://ftp.vim.org/pub/vim/patches/7.4/7.4.010
Patch011: http://ftp.vim.org/pub/vim/patches/7.4/7.4.011
Patch012: http://ftp.vim.org/pub/vim/patches/7.4/7.4.012
Patch013: http://ftp.vim.org/pub/vim/patches/7.4/7.4.013
Patch014: http://ftp.vim.org/pub/vim/patches/7.4/7.4.014
Patch015: http://ftp.vim.org/pub/vim/patches/7.4/7.4.015
Patch016: http://ftp.vim.org/pub/vim/patches/7.4/7.4.016
Patch017: http://ftp.vim.org/pub/vim/patches/7.4/7.4.017
Patch018: http://ftp.vim.org/pub/vim/patches/7.4/7.4.018
Patch019: http://ftp.vim.org/pub/vim/patches/7.4/7.4.019
Patch020: http://ftp.vim.org/pub/vim/patches/7.4/7.4.020
Patch021: http://ftp.vim.org/pub/vim/patches/7.4/7.4.021
Patch022: http://ftp.vim.org/pub/vim/patches/7.4/7.4.022
Patch023: http://ftp.vim.org/pub/vim/patches/7.4/7.4.023
Patch024: http://ftp.vim.org/pub/vim/patches/7.4/7.4.024
Patch025: http://ftp.vim.org/pub/vim/patches/7.4/7.4.025
Patch026: http://ftp.vim.org/pub/vim/patches/7.4/7.4.026
Patch027: http://ftp.vim.org/pub/vim/patches/7.4/7.4.027
Patch028: http://ftp.vim.org/pub/vim/patches/7.4/7.4.028
Patch029: http://ftp.vim.org/pub/vim/patches/7.4/7.4.029
Patch030: http://ftp.vim.org/pub/vim/patches/7.4/7.4.030
Patch031: http://ftp.vim.org/pub/vim/patches/7.4/7.4.031
Patch032: http://ftp.vim.org/pub/vim/patches/7.4/7.4.032
Patch033: http://ftp.vim.org/pub/vim/patches/7.4/7.4.033
Patch034: http://ftp.vim.org/pub/vim/patches/7.4/7.4.034
Patch035: http://ftp.vim.org/pub/vim/patches/7.4/7.4.035
Patch036: http://ftp.vim.org/pub/vim/patches/7.4/7.4.036
Patch037: http://ftp.vim.org/pub/vim/patches/7.4/7.4.037
Patch038: http://ftp.vim.org/pub/vim/patches/7.4/7.4.038
Patch039: http://ftp.vim.org/pub/vim/patches/7.4/7.4.039
Patch040: http://ftp.vim.org/pub/vim/patches/7.4/7.4.040
Patch041: http://ftp.vim.org/pub/vim/patches/7.4/7.4.041
Patch042: http://ftp.vim.org/pub/vim/patches/7.4/7.4.042
Patch043: http://ftp.vim.org/pub/vim/patches/7.4/7.4.043
Patch044: http://ftp.vim.org/pub/vim/patches/7.4/7.4.044
Patch045: http://ftp.vim.org/pub/vim/patches/7.4/7.4.045
Patch046: http://ftp.vim.org/pub/vim/patches/7.4/7.4.046
Patch047: http://ftp.vim.org/pub/vim/patches/7.4/7.4.047
Patch048: http://ftp.vim.org/pub/vim/patches/7.4/7.4.048
Patch049: http://ftp.vim.org/pub/vim/patches/7.4/7.4.049
Patch050: http://ftp.vim.org/pub/vim/patches/7.4/7.4.050
Patch051: http://ftp.vim.org/pub/vim/patches/7.4/7.4.051
Patch052: http://ftp.vim.org/pub/vim/patches/7.4/7.4.052
Patch053: http://ftp.vim.org/pub/vim/patches/7.4/7.4.053
Patch054: http://ftp.vim.org/pub/vim/patches/7.4/7.4.054
Patch055: http://ftp.vim.org/pub/vim/patches/7.4/7.4.055
Patch056: http://ftp.vim.org/pub/vim/patches/7.4/7.4.056
Patch057: http://ftp.vim.org/pub/vim/patches/7.4/7.4.057
Patch058: http://ftp.vim.org/pub/vim/patches/7.4/7.4.058
Patch059: http://ftp.vim.org/pub/vim/patches/7.4/7.4.059
Patch060: http://ftp.vim.org/pub/vim/patches/7.4/7.4.060
Patch061: http://ftp.vim.org/pub/vim/patches/7.4/7.4.061
Patch062: http://ftp.vim.org/pub/vim/patches/7.4/7.4.062
Patch063: http://ftp.vim.org/pub/vim/patches/7.4/7.4.063
Patch064: http://ftp.vim.org/pub/vim/patches/7.4/7.4.064
Patch065: http://ftp.vim.org/pub/vim/patches/7.4/7.4.065
Patch066: http://ftp.vim.org/pub/vim/patches/7.4/7.4.066
Patch067: http://ftp.vim.org/pub/vim/patches/7.4/7.4.067
Patch068: http://ftp.vim.org/pub/vim/patches/7.4/7.4.068
Patch069: http://ftp.vim.org/pub/vim/patches/7.4/7.4.069
Patch070: http://ftp.vim.org/pub/vim/patches/7.4/7.4.070
Patch071: http://ftp.vim.org/pub/vim/patches/7.4/7.4.071
Patch072: http://ftp.vim.org/pub/vim/patches/7.4/7.4.072
Patch073: http://ftp.vim.org/pub/vim/patches/7.4/7.4.073
Patch074: http://ftp.vim.org/pub/vim/patches/7.4/7.4.074
Patch075: http://ftp.vim.org/pub/vim/patches/7.4/7.4.075
Patch076: http://ftp.vim.org/pub/vim/patches/7.4/7.4.076
Patch077: http://ftp.vim.org/pub/vim/patches/7.4/7.4.077
Patch078: http://ftp.vim.org/pub/vim/patches/7.4/7.4.078
Patch079: http://ftp.vim.org/pub/vim/patches/7.4/7.4.079
Patch080: http://ftp.vim.org/pub/vim/patches/7.4/7.4.080
Patch081: http://ftp.vim.org/pub/vim/patches/7.4/7.4.081
Patch082: http://ftp.vim.org/pub/vim/patches/7.4/7.4.082
Patch083: http://ftp.vim.org/pub/vim/patches/7.4/7.4.083
Patch084: http://ftp.vim.org/pub/vim/patches/7.4/7.4.084
Patch085: http://ftp.vim.org/pub/vim/patches/7.4/7.4.085
Patch086: http://ftp.vim.org/pub/vim/patches/7.4/7.4.086
Patch087: http://ftp.vim.org/pub/vim/patches/7.4/7.4.087
Patch088: http://ftp.vim.org/pub/vim/patches/7.4/7.4.088
Patch089: http://ftp.vim.org/pub/vim/patches/7.4/7.4.089
Patch090: http://ftp.vim.org/pub/vim/patches/7.4/7.4.090
Patch091: http://ftp.vim.org/pub/vim/patches/7.4/7.4.091
Patch092: http://ftp.vim.org/pub/vim/patches/7.4/7.4.092
Patch093: http://ftp.vim.org/pub/vim/patches/7.4/7.4.093
Patch094: http://ftp.vim.org/pub/vim/patches/7.4/7.4.094
Patch095: http://ftp.vim.org/pub/vim/patches/7.4/7.4.095
Patch096: http://ftp.vim.org/pub/vim/patches/7.4/7.4.096
Patch097: http://ftp.vim.org/pub/vim/patches/7.4/7.4.097
Patch098: http://ftp.vim.org/pub/vim/patches/7.4/7.4.098
Patch099: http://ftp.vim.org/pub/vim/patches/7.4/7.4.099
Patch100: http://ftp.vim.org/pub/vim/patches/7.4/7.4.100
Patch101: http://ftp.vim.org/pub/vim/patches/7.4/7.4.101
Patch102: http://ftp.vim.org/pub/vim/patches/7.4/7.4.102
Patch103: http://ftp.vim.org/pub/vim/patches/7.4/7.4.103
Patch104: http://ftp.vim.org/pub/vim/patches/7.4/7.4.104
Patch105: http://ftp.vim.org/pub/vim/patches/7.4/7.4.105
Patch106: http://ftp.vim.org/pub/vim/patches/7.4/7.4.106
Patch107: http://ftp.vim.org/pub/vim/patches/7.4/7.4.107
Patch108: http://ftp.vim.org/pub/vim/patches/7.4/7.4.108
Patch109: http://ftp.vim.org/pub/vim/patches/7.4/7.4.109
Patch110: http://ftp.vim.org/pub/vim/patches/7.4/7.4.110
Patch111: http://ftp.vim.org/pub/vim/patches/7.4/7.4.111
Patch112: http://ftp.vim.org/pub/vim/patches/7.4/7.4.112
Patch113: http://ftp.vim.org/pub/vim/patches/7.4/7.4.113
Patch114: http://ftp.vim.org/pub/vim/patches/7.4/7.4.114
Patch115: http://ftp.vim.org/pub/vim/patches/7.4/7.4.115
Patch116: http://ftp.vim.org/pub/vim/patches/7.4/7.4.116
Patch117: http://ftp.vim.org/pub/vim/patches/7.4/7.4.117
Patch118: http://ftp.vim.org/pub/vim/patches/7.4/7.4.118
Patch119: http://ftp.vim.org/pub/vim/patches/7.4/7.4.119
Patch120: http://ftp.vim.org/pub/vim/patches/7.4/7.4.120
Patch121: http://ftp.vim.org/pub/vim/patches/7.4/7.4.121
Patch122: http://ftp.vim.org/pub/vim/patches/7.4/7.4.122
Patch123: http://ftp.vim.org/pub/vim/patches/7.4/7.4.123
Patch124: http://ftp.vim.org/pub/vim/patches/7.4/7.4.124
Patch125: http://ftp.vim.org/pub/vim/patches/7.4/7.4.125
Patch126: http://ftp.vim.org/pub/vim/patches/7.4/7.4.126
Patch127: http://ftp.vim.org/pub/vim/patches/7.4/7.4.127
Patch128: http://ftp.vim.org/pub/vim/patches/7.4/7.4.128
Patch129: http://ftp.vim.org/pub/vim/patches/7.4/7.4.129
Patch130: http://ftp.vim.org/pub/vim/patches/7.4/7.4.130
Patch131: http://ftp.vim.org/pub/vim/patches/7.4/7.4.131
Patch132: http://ftp.vim.org/pub/vim/patches/7.4/7.4.132
Patch133: http://ftp.vim.org/pub/vim/patches/7.4/7.4.133
Patch134: http://ftp.vim.org/pub/vim/patches/7.4/7.4.134
Patch135: http://ftp.vim.org/pub/vim/patches/7.4/7.4.135
Patch136: http://ftp.vim.org/pub/vim/patches/7.4/7.4.136
Patch137: http://ftp.vim.org/pub/vim/patches/7.4/7.4.137
Patch138: http://ftp.vim.org/pub/vim/patches/7.4/7.4.138
Patch139: http://ftp.vim.org/pub/vim/patches/7.4/7.4.139
Patch140: http://ftp.vim.org/pub/vim/patches/7.4/7.4.140
Patch141: http://ftp.vim.org/pub/vim/patches/7.4/7.4.141
Patch142: http://ftp.vim.org/pub/vim/patches/7.4/7.4.142
Patch143: http://ftp.vim.org/pub/vim/patches/7.4/7.4.143
Patch144: http://ftp.vim.org/pub/vim/patches/7.4/7.4.144
Patch145: http://ftp.vim.org/pub/vim/patches/7.4/7.4.145
Patch146: http://ftp.vim.org/pub/vim/patches/7.4/7.4.146
Patch147: http://ftp.vim.org/pub/vim/patches/7.4/7.4.147
Patch148: http://ftp.vim.org/pub/vim/patches/7.4/7.4.148
Patch149: http://ftp.vim.org/pub/vim/patches/7.4/7.4.149
Patch150: http://ftp.vim.org/pub/vim/patches/7.4/7.4.150
Patch151: http://ftp.vim.org/pub/vim/patches/7.4/7.4.151
Patch152: http://ftp.vim.org/pub/vim/patches/7.4/7.4.152
Patch153: http://ftp.vim.org/pub/vim/patches/7.4/7.4.153
Patch154: http://ftp.vim.org/pub/vim/patches/7.4/7.4.154
Patch155: http://ftp.vim.org/pub/vim/patches/7.4/7.4.155
Patch156: http://ftp.vim.org/pub/vim/patches/7.4/7.4.156
Patch157: http://ftp.vim.org/pub/vim/patches/7.4/7.4.157
Patch158: http://ftp.vim.org/pub/vim/patches/7.4/7.4.158
Patch159: http://ftp.vim.org/pub/vim/patches/7.4/7.4.159
Patch160: http://ftp.vim.org/pub/vim/patches/7.4/7.4.160
Patch161: http://ftp.vim.org/pub/vim/patches/7.4/7.4.161
Patch162: http://ftp.vim.org/pub/vim/patches/7.4/7.4.162
Patch163: http://ftp.vim.org/pub/vim/patches/7.4/7.4.163
Patch164: http://ftp.vim.org/pub/vim/patches/7.4/7.4.164
Patch165: http://ftp.vim.org/pub/vim/patches/7.4/7.4.165
Patch166: http://ftp.vim.org/pub/vim/patches/7.4/7.4.166
Patch167: http://ftp.vim.org/pub/vim/patches/7.4/7.4.167
Patch168: http://ftp.vim.org/pub/vim/patches/7.4/7.4.168
Patch169: http://ftp.vim.org/pub/vim/patches/7.4/7.4.169
Patch170: http://ftp.vim.org/pub/vim/patches/7.4/7.4.170
Patch171: http://ftp.vim.org/pub/vim/patches/7.4/7.4.171
Patch172: http://ftp.vim.org/pub/vim/patches/7.4/7.4.172
Patch173: http://ftp.vim.org/pub/vim/patches/7.4/7.4.173
Patch174: http://ftp.vim.org/pub/vim/patches/7.4/7.4.174
Patch175: http://ftp.vim.org/pub/vim/patches/7.4/7.4.175
Patch176: http://ftp.vim.org/pub/vim/patches/7.4/7.4.176
Patch177: http://ftp.vim.org/pub/vim/patches/7.4/7.4.177
Patch178: http://ftp.vim.org/pub/vim/patches/7.4/7.4.178
Patch179: http://ftp.vim.org/pub/vim/patches/7.4/7.4.179
Patch180: http://ftp.vim.org/pub/vim/patches/7.4/7.4.180
Patch181: http://ftp.vim.org/pub/vim/patches/7.4/7.4.181
Patch182: http://ftp.vim.org/pub/vim/patches/7.4/7.4.182
Patch183: http://ftp.vim.org/pub/vim/patches/7.4/7.4.183
Patch184: http://ftp.vim.org/pub/vim/patches/7.4/7.4.184
Patch185: http://ftp.vim.org/pub/vim/patches/7.4/7.4.185
Patch186: http://ftp.vim.org/pub/vim/patches/7.4/7.4.186
Patch187: http://ftp.vim.org/pub/vim/patches/7.4/7.4.187
Patch188: http://ftp.vim.org/pub/vim/patches/7.4/7.4.188
Patch189: http://ftp.vim.org/pub/vim/patches/7.4/7.4.189
Patch190: http://ftp.vim.org/pub/vim/patches/7.4/7.4.190
Patch191: http://ftp.vim.org/pub/vim/patches/7.4/7.4.191
Patch192: http://ftp.vim.org/pub/vim/patches/7.4/7.4.192
Patch193: http://ftp.vim.org/pub/vim/patches/7.4/7.4.193
Patch194: http://ftp.vim.org/pub/vim/patches/7.4/7.4.194
Patch195: http://ftp.vim.org/pub/vim/patches/7.4/7.4.195
Patch196: http://ftp.vim.org/pub/vim/patches/7.4/7.4.196
Patch197: http://ftp.vim.org/pub/vim/patches/7.4/7.4.197
Patch198: http://ftp.vim.org/pub/vim/patches/7.4/7.4.198
Patch199: http://ftp.vim.org/pub/vim/patches/7.4/7.4.199
Patch200: http://ftp.vim.org/pub/vim/patches/7.4/7.4.200
Patch201: http://ftp.vim.org/pub/vim/patches/7.4/7.4.201
Patch202: http://ftp.vim.org/pub/vim/patches/7.4/7.4.202
Patch203: http://ftp.vim.org/pub/vim/patches/7.4/7.4.203
Patch204: http://ftp.vim.org/pub/vim/patches/7.4/7.4.204
Patch205: http://ftp.vim.org/pub/vim/patches/7.4/7.4.205
Patch206: http://ftp.vim.org/pub/vim/patches/7.4/7.4.206
Patch207: http://ftp.vim.org/pub/vim/patches/7.4/7.4.207
Patch208: http://ftp.vim.org/pub/vim/patches/7.4/7.4.208
Patch209: http://ftp.vim.org/pub/vim/patches/7.4/7.4.209
Patch210: http://ftp.vim.org/pub/vim/patches/7.4/7.4.210
Patch211: http://ftp.vim.org/pub/vim/patches/7.4/7.4.211
Patch212: http://ftp.vim.org/pub/vim/patches/7.4/7.4.212
Patch213: http://ftp.vim.org/pub/vim/patches/7.4/7.4.213
Patch214: http://ftp.vim.org/pub/vim/patches/7.4/7.4.214
Patch215: http://ftp.vim.org/pub/vim/patches/7.4/7.4.215
Patch216: http://ftp.vim.org/pub/vim/patches/7.4/7.4.216
Patch217: http://ftp.vim.org/pub/vim/patches/7.4/7.4.217
Patch218: http://ftp.vim.org/pub/vim/patches/7.4/7.4.218
Patch219: http://ftp.vim.org/pub/vim/patches/7.4/7.4.219
Patch220: http://ftp.vim.org/pub/vim/patches/7.4/7.4.220
Patch221: http://ftp.vim.org/pub/vim/patches/7.4/7.4.221
Patch222: http://ftp.vim.org/pub/vim/patches/7.4/7.4.222
Patch223: http://ftp.vim.org/pub/vim/patches/7.4/7.4.223
Patch224: http://ftp.vim.org/pub/vim/patches/7.4/7.4.224
Patch225: http://ftp.vim.org/pub/vim/patches/7.4/7.4.225
Patch226: http://ftp.vim.org/pub/vim/patches/7.4/7.4.226
Patch227: http://ftp.vim.org/pub/vim/patches/7.4/7.4.227
Patch228: http://ftp.vim.org/pub/vim/patches/7.4/7.4.228
Patch229: http://ftp.vim.org/pub/vim/patches/7.4/7.4.229
Patch230: http://ftp.vim.org/pub/vim/patches/7.4/7.4.230
Patch231: http://ftp.vim.org/pub/vim/patches/7.4/7.4.231
Patch232: http://ftp.vim.org/pub/vim/patches/7.4/7.4.232
Patch233: http://ftp.vim.org/pub/vim/patches/7.4/7.4.233
Patch234: http://ftp.vim.org/pub/vim/patches/7.4/7.4.234
Patch235: http://ftp.vim.org/pub/vim/patches/7.4/7.4.235
Patch236: http://ftp.vim.org/pub/vim/patches/7.4/7.4.236
Patch237: http://ftp.vim.org/pub/vim/patches/7.4/7.4.237
Patch238: http://ftp.vim.org/pub/vim/patches/7.4/7.4.238
Patch239: http://ftp.vim.org/pub/vim/patches/7.4/7.4.239
Patch240: http://ftp.vim.org/pub/vim/patches/7.4/7.4.240
Patch241: http://ftp.vim.org/pub/vim/patches/7.4/7.4.241
Patch242: http://ftp.vim.org/pub/vim/patches/7.4/7.4.242
Patch243: http://ftp.vim.org/pub/vim/patches/7.4/7.4.243
Patch244: http://ftp.vim.org/pub/vim/patches/7.4/7.4.244
Patch245: http://ftp.vim.org/pub/vim/patches/7.4/7.4.245
Patch246: http://ftp.vim.org/pub/vim/patches/7.4/7.4.246
Patch247: http://ftp.vim.org/pub/vim/patches/7.4/7.4.247
Patch248: http://ftp.vim.org/pub/vim/patches/7.4/7.4.248
Patch249: http://ftp.vim.org/pub/vim/patches/7.4/7.4.249
Patch250: http://ftp.vim.org/pub/vim/patches/7.4/7.4.250
Patch251: http://ftp.vim.org/pub/vim/patches/7.4/7.4.251
Patch252: http://ftp.vim.org/pub/vim/patches/7.4/7.4.252
Patch253: http://ftp.vim.org/pub/vim/patches/7.4/7.4.253
Patch254: http://ftp.vim.org/pub/vim/patches/7.4/7.4.254
Patch255: http://ftp.vim.org/pub/vim/patches/7.4/7.4.255
Patch256: http://ftp.vim.org/pub/vim/patches/7.4/7.4.256
Patch257: http://ftp.vim.org/pub/vim/patches/7.4/7.4.257
Patch258: http://ftp.vim.org/pub/vim/patches/7.4/7.4.258
Patch259: http://ftp.vim.org/pub/vim/patches/7.4/7.4.259
Patch260: http://ftp.vim.org/pub/vim/patches/7.4/7.4.260
Patch261: http://ftp.vim.org/pub/vim/patches/7.4/7.4.261
Patch262: http://ftp.vim.org/pub/vim/patches/7.4/7.4.262
Patch263: http://ftp.vim.org/pub/vim/patches/7.4/7.4.263
Patch264: http://ftp.vim.org/pub/vim/patches/7.4/7.4.264
Patch265: http://ftp.vim.org/pub/vim/patches/7.4/7.4.265
Patch266: http://ftp.vim.org/pub/vim/patches/7.4/7.4.266
Patch267: http://ftp.vim.org/pub/vim/patches/7.4/7.4.267
Patch268: http://ftp.vim.org/pub/vim/patches/7.4/7.4.268
Patch269: http://ftp.vim.org/pub/vim/patches/7.4/7.4.269
Patch270: http://ftp.vim.org/pub/vim/patches/7.4/7.4.270
Patch271: http://ftp.vim.org/pub/vim/patches/7.4/7.4.271
Patch272: http://ftp.vim.org/pub/vim/patches/7.4/7.4.272
Patch273: http://ftp.vim.org/pub/vim/patches/7.4/7.4.273
Patch274: http://ftp.vim.org/pub/vim/patches/7.4/7.4.274
Patch275: http://ftp.vim.org/pub/vim/patches/7.4/7.4.275
Patch276: http://ftp.vim.org/pub/vim/patches/7.4/7.4.276
Patch277: http://ftp.vim.org/pub/vim/patches/7.4/7.4.277
Patch278: http://ftp.vim.org/pub/vim/patches/7.4/7.4.278
Patch279: http://ftp.vim.org/pub/vim/patches/7.4/7.4.279
Patch280: http://ftp.vim.org/pub/vim/patches/7.4/7.4.280
Patch281: http://ftp.vim.org/pub/vim/patches/7.4/7.4.281
Patch282: http://ftp.vim.org/pub/vim/patches/7.4/7.4.282
Patch283: http://ftp.vim.org/pub/vim/patches/7.4/7.4.283
Patch284: http://ftp.vim.org/pub/vim/patches/7.4/7.4.284
Patch285: http://ftp.vim.org/pub/vim/patches/7.4/7.4.285
Patch286: http://ftp.vim.org/pub/vim/patches/7.4/7.4.286
Patch287: http://ftp.vim.org/pub/vim/patches/7.4/7.4.287
Patch288: http://ftp.vim.org/pub/vim/patches/7.4/7.4.288
Patch289: http://ftp.vim.org/pub/vim/patches/7.4/7.4.289
Patch290: http://ftp.vim.org/pub/vim/patches/7.4/7.4.290
Patch291: http://ftp.vim.org/pub/vim/patches/7.4/7.4.291
Patch292: http://ftp.vim.org/pub/vim/patches/7.4/7.4.292
Patch293: http://ftp.vim.org/pub/vim/patches/7.4/7.4.293
Patch294: http://ftp.vim.org/pub/vim/patches/7.4/7.4.294
Patch295: http://ftp.vim.org/pub/vim/patches/7.4/7.4.295
Patch296: http://ftp.vim.org/pub/vim/patches/7.4/7.4.296
Patch297: http://ftp.vim.org/pub/vim/patches/7.4/7.4.297
Patch298: http://ftp.vim.org/pub/vim/patches/7.4/7.4.298
Patch299: http://ftp.vim.org/pub/vim/patches/7.4/7.4.299
Patch300: http://ftp.vim.org/pub/vim/patches/7.4/7.4.300
Patch301: http://ftp.vim.org/pub/vim/patches/7.4/7.4.301
Patch302: http://ftp.vim.org/pub/vim/patches/7.4/7.4.302
Patch303: http://ftp.vim.org/pub/vim/patches/7.4/7.4.303
Patch304: http://ftp.vim.org/pub/vim/patches/7.4/7.4.304
Patch305: http://ftp.vim.org/pub/vim/patches/7.4/7.4.305
Patch306: http://ftp.vim.org/pub/vim/patches/7.4/7.4.306
Patch307: http://ftp.vim.org/pub/vim/patches/7.4/7.4.307
Patch308: http://ftp.vim.org/pub/vim/patches/7.4/7.4.308
Patch309: http://ftp.vim.org/pub/vim/patches/7.4/7.4.309
Patch310: http://ftp.vim.org/pub/vim/patches/7.4/7.4.310
Patch311: http://ftp.vim.org/pub/vim/patches/7.4/7.4.311
Patch312: http://ftp.vim.org/pub/vim/patches/7.4/7.4.312
Patch313: http://ftp.vim.org/pub/vim/patches/7.4/7.4.313
Patch314: http://ftp.vim.org/pub/vim/patches/7.4/7.4.314
Patch315: http://ftp.vim.org/pub/vim/patches/7.4/7.4.315
Patch316: http://ftp.vim.org/pub/vim/patches/7.4/7.4.316
Patch317: http://ftp.vim.org/pub/vim/patches/7.4/7.4.317
Patch318: http://ftp.vim.org/pub/vim/patches/7.4/7.4.318
Patch319: http://ftp.vim.org/pub/vim/patches/7.4/7.4.319
Patch320: http://ftp.vim.org/pub/vim/patches/7.4/7.4.320
Patch321: http://ftp.vim.org/pub/vim/patches/7.4/7.4.321
Patch322: http://ftp.vim.org/pub/vim/patches/7.4/7.4.322
Patch323: http://ftp.vim.org/pub/vim/patches/7.4/7.4.323
Patch324: http://ftp.vim.org/pub/vim/patches/7.4/7.4.324
Patch325: http://ftp.vim.org/pub/vim/patches/7.4/7.4.325
Patch326: http://ftp.vim.org/pub/vim/patches/7.4/7.4.326
Patch327: http://ftp.vim.org/pub/vim/patches/7.4/7.4.327
Patch328: http://ftp.vim.org/pub/vim/patches/7.4/7.4.328
Patch329: http://ftp.vim.org/pub/vim/patches/7.4/7.4.329
Patch330: http://ftp.vim.org/pub/vim/patches/7.4/7.4.330
Patch331: http://ftp.vim.org/pub/vim/patches/7.4/7.4.331
Patch332: http://ftp.vim.org/pub/vim/patches/7.4/7.4.332
Patch333: http://ftp.vim.org/pub/vim/patches/7.4/7.4.333
Patch334: http://ftp.vim.org/pub/vim/patches/7.4/7.4.334
Patch335: http://ftp.vim.org/pub/vim/patches/7.4/7.4.335
Patch336: http://ftp.vim.org/pub/vim/patches/7.4/7.4.336
Patch337: http://ftp.vim.org/pub/vim/patches/7.4/7.4.337
Patch338: http://ftp.vim.org/pub/vim/patches/7.4/7.4.338
Patch339: http://ftp.vim.org/pub/vim/patches/7.4/7.4.339
Patch340: http://ftp.vim.org/pub/vim/patches/7.4/7.4.340
Patch341: http://ftp.vim.org/pub/vim/patches/7.4/7.4.341
Patch342: http://ftp.vim.org/pub/vim/patches/7.4/7.4.342
Patch343: http://ftp.vim.org/pub/vim/patches/7.4/7.4.343
Patch344: http://ftp.vim.org/pub/vim/patches/7.4/7.4.344
Patch345: http://ftp.vim.org/pub/vim/patches/7.4/7.4.345
Patch346: http://ftp.vim.org/pub/vim/patches/7.4/7.4.346
Patch347: http://ftp.vim.org/pub/vim/patches/7.4/7.4.347
Patch348: http://ftp.vim.org/pub/vim/patches/7.4/7.4.348
Patch349: http://ftp.vim.org/pub/vim/patches/7.4/7.4.349
Patch350: http://ftp.vim.org/pub/vim/patches/7.4/7.4.350
Patch351: http://ftp.vim.org/pub/vim/patches/7.4/7.4.351
Patch352: http://ftp.vim.org/pub/vim/patches/7.4/7.4.352
Patch353: http://ftp.vim.org/pub/vim/patches/7.4/7.4.353
Patch354: http://ftp.vim.org/pub/vim/patches/7.4/7.4.354
Patch355: http://ftp.vim.org/pub/vim/patches/7.4/7.4.355
Patch356: http://ftp.vim.org/pub/vim/patches/7.4/7.4.356
Patch357: http://ftp.vim.org/pub/vim/patches/7.4/7.4.357
Patch358: http://ftp.vim.org/pub/vim/patches/7.4/7.4.358
Patch359: http://ftp.vim.org/pub/vim/patches/7.4/7.4.359
Patch360: http://ftp.vim.org/pub/vim/patches/7.4/7.4.360
Patch361: http://ftp.vim.org/pub/vim/patches/7.4/7.4.361
Patch362: http://ftp.vim.org/pub/vim/patches/7.4/7.4.362
Patch363: http://ftp.vim.org/pub/vim/patches/7.4/7.4.363
Patch364: http://ftp.vim.org/pub/vim/patches/7.4/7.4.364
Patch365: http://ftp.vim.org/pub/vim/patches/7.4/7.4.365
Patch366: http://ftp.vim.org/pub/vim/patches/7.4/7.4.366
Patch367: http://ftp.vim.org/pub/vim/patches/7.4/7.4.367
Patch368: http://ftp.vim.org/pub/vim/patches/7.4/7.4.368
Patch369: http://ftp.vim.org/pub/vim/patches/7.4/7.4.369
Patch370: http://ftp.vim.org/pub/vim/patches/7.4/7.4.370
Patch371: http://ftp.vim.org/pub/vim/patches/7.4/7.4.371
Patch372: http://ftp.vim.org/pub/vim/patches/7.4/7.4.372
Patch373: http://ftp.vim.org/pub/vim/patches/7.4/7.4.373
Patch374: http://ftp.vim.org/pub/vim/patches/7.4/7.4.374
Patch375: http://ftp.vim.org/pub/vim/patches/7.4/7.4.375
Patch376: http://ftp.vim.org/pub/vim/patches/7.4/7.4.376
Patch377: http://ftp.vim.org/pub/vim/patches/7.4/7.4.377
Patch378: http://ftp.vim.org/pub/vim/patches/7.4/7.4.378
Patch379: http://ftp.vim.org/pub/vim/patches/7.4/7.4.379
Patch380: http://ftp.vim.org/pub/vim/patches/7.4/7.4.380
Patch381: http://ftp.vim.org/pub/vim/patches/7.4/7.4.381
Patch382: http://ftp.vim.org/pub/vim/patches/7.4/7.4.382
Patch383: http://ftp.vim.org/pub/vim/patches/7.4/7.4.383
Patch384: http://ftp.vim.org/pub/vim/patches/7.4/7.4.384
Patch385: http://ftp.vim.org/pub/vim/patches/7.4/7.4.385
Patch386: http://ftp.vim.org/pub/vim/patches/7.4/7.4.386
Patch387: http://ftp.vim.org/pub/vim/patches/7.4/7.4.387
Patch388: http://ftp.vim.org/pub/vim/patches/7.4/7.4.388
Patch389: http://ftp.vim.org/pub/vim/patches/7.4/7.4.389


Patch3000: vim-7.4-no_link_as_needed.patch
Patch3002: vim-7.1-nowarnings.patch
Patch3004: vim-7.0-rclocation.patch
Patch3006: vim-6.4-checkhl.patch
Patch3007: vim-7.4-fstabsyntax.patch
Patch3008: vim-7.0-warning.patch
Patch3009: vim-7.0-syncolor.patch
Patch3010: vim-7.0-specedit.patch
Patch3011: vim72-rh514717.patch
Patch3012: vim-7.3-manpage-typo-668894-675480.patch
Patch3013: vim-7.3-xsubpp-path.patch
Patch3014: vim-manpagefixes-948566.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-devel ncurses-devel gettext
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: libacl-devel autoconf
%if %{WITH_SELINUX}
BuildRequires: libselinux-devel
%endif
%if "%{withruby}" == "1"
Buildrequires: ruby-devel ruby
%endif
%if %{desktop_file}
# for /usr/bin/desktop-file-install
Requires: desktop-file-utils
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
%endif
Requires: vim-common = %{epoch}:%{version}-%{release}
Epoch: 2

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.

%package common
Summary: The common files needed by any version of the VIM editor
Group: Applications/Editors
Conflicts: man-pages-fr < 0.9.7-14
Conflicts: man-pages-it < 0.3.0-17
Conflicts: man-pages-pl < 0.24-2
Requires: vim-filesystem = %{epoch}:%{version}-%{release}

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-common package contains files which every VIM binary will need in
order to run.

If you are installing vim-enhanced or vim-X11, you'll also need
to install the vim-common package.

%package spell
Summary: The dictionaries for spell checking. This package is optional
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release}

%description spell
This subpackage contains dictionaries for vim spell checking in
many different languages.

%package minimal
Summary: A minimal version of the VIM editor
Group: Applications/Editors
Provides: vi = %{version}-%{release}

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more. The
vim-minimal package includes a minimal version of VIM, which is
installed into /bin/vi for use when only the root partition is
present. NOTE: The online help is only available when the vim-common
package is installed.

%package enhanced
Summary: A version of the VIM editor which includes recent enhancements
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release} which
Provides: vim = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with extra, recently
introduced features like Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the
VIM editor which includes recently added enhancements like
interpreters for the Python and Perl scripting languages.  You'll also
need to install the vim-common package.

%package filesystem
Summary: VIM filesystem layout
Group: Applications/Editors

%Description filesystem
This package provides some directories which are required by other
packages that add vim files, p.e.  additional syntax files or filetypes.

%package X11
Summary: The VIM version of the vi editor for the X Window System
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release} libattr >= 2.4 gtk2 >= 2.6
Provides: gvim = %{version}-%{release}
BuildRequires: gtk2-devel libSM-devel libXt-devel libXpm-devel
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: hicolor-icon-theme

%description X11
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and
more. VIM-X11 is a version of the VIM editor which will run within the
X Window System.  If you install this package, you can run VIM as an X
application with a full GUI interface and mouse support.

Install the vim-X11 package if you'd like to try out a version of vi
with graphics and mouse capabilities.  You'll also need to install the
vim-common package.

%prep
%setup -q -b 0 -n %{vimdir}
# fix rogue dependencies from sample code
chmod -x runtime/tools/mve.awk
perl -pi -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk

%patch001 -p0
%patch002 -p0
%patch003 -p0
%patch004 -p0
%patch005 -p0
%patch006 -p0
%patch007 -p0
%patch008 -p0
%patch009 -p0
%patch010 -p0
%patch011 -p0
%patch012 -p0
%patch013 -p0
%patch014 -p0
%patch015 -p0
%patch016 -p0
%patch017 -p0
%patch018 -p0
%patch019 -p0
%patch020 -p0
%patch021 -p0
%patch022 -p0
%patch023 -p0
%patch024 -p0
%patch025 -p0
%patch026 -p0
%patch027 -p0
%patch028 -p0
%patch029 -p0
%patch030 -p0
%patch031 -p0
%patch032 -p0
%patch033 -p0
%patch034 -p0
%patch035 -p0
%patch036 -p0
%patch037 -p0
%patch038 -p0
%patch039 -p0
%patch040 -p0
%patch041 -p0
%patch042 -p0
%patch043 -p0
%patch044 -p0
%patch045 -p0
%patch046 -p0
%patch047 -p0
%patch048 -p0
%patch049 -p0
%patch050 -p0
%patch051 -p0
%patch052 -p0
%patch053 -p0
%patch054 -p0
%patch055 -p0
%patch056 -p0
%patch057 -p0
%patch058 -p0
%patch059 -p0
%patch060 -p0
%patch061 -p0
%patch062 -p0
%patch063 -p0
%patch064 -p0
%patch065 -p0
%patch066 -p0
%patch067 -p0
%patch068 -p0
%patch069 -p0
%patch070 -p0
%patch071 -p0
%patch072 -p0
%patch073 -p0
%patch074 -p0
%patch075 -p0
%patch076 -p0
%patch077 -p0
%patch078 -p0
%patch079 -p0
%patch080 -p0
%patch081 -p0
%patch082 -p0
%patch083 -p0
%patch084 -p0
%patch085 -p0
%patch086 -p0
%patch087 -p0
%patch088 -p0
%patch089 -p0
%patch090 -p0
%patch091 -p0
%patch092 -p0
%patch093 -p0
%patch094 -p0
%patch095 -p0
%patch096 -p0
%patch097 -p0
%patch098 -p0
%patch099 -p0
%patch100 -p0
%patch101 -p0
%patch102 -p0
%patch103 -p0
%patch104 -p0
%patch105 -p0
%patch106 -p0
%patch107 -p0
%patch108 -p0
%patch109 -p0
%patch110 -p0
%patch111 -p0
%patch112 -p0
%patch113 -p0
%patch114 -p0
%patch115 -p0
%patch116 -p0
%patch117 -p0
%patch118 -p0
%patch119 -p0
%patch120 -p0
%patch121 -p0
%patch122 -p0
%patch123 -p0
%patch124 -p0
%patch125 -p0
%patch126 -p0
%patch127 -p0
%patch128 -p0
%patch129 -p0
%patch130 -p0
%patch131 -p0
%patch132 -p0
%patch133 -p0
%patch134 -p0
%patch135 -p0
%patch136 -p0
%patch137 -p0
%patch138 -p0
%patch139 -p0
%patch140 -p0
%patch141 -p0
%patch142 -p0
%patch143 -p0
%patch144 -p0
%patch145 -p0
%patch146 -p0
%patch147 -p0
%patch148 -p0
%patch149 -p0
%patch150 -p0
%patch151 -p0
%patch152 -p0
%patch153 -p0
%patch154 -p0
%patch155 -p0
%patch156 -p0
%patch157 -p0
%patch158 -p0
%patch159 -p0
%patch160 -p0
%patch161 -p0

%patch3000 -p1
%patch3002 -p1
%patch3004 -p1
%patch3006 -p1
%patch3007 -p1
%patch3008 -p1
%patch3009 -p1
%patch3010 -p1
%patch3011 -p1
%patch3012 -p1

%if %{?fedora}%{!?fedora:0} >= 20 || %{?rhel}%{!?rhel:0} >= 7
%patch3013 -p1
%endif
%patch3014 -p1

# install spell files
%if %{withvimspell}
%{__tar} xjf %{SOURCE13}
%endif

%build
cd src
autoconf

echo '#define SYS_VIMRC_FILE  "/etc/vimrc"' >> feature.h

export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"

%configure --with-features=huge --enable-pythoninterp --enable-perlinterp \
  --disable-tclinterp --with-x=yes \
  --enable-xim --enable-multibyte \
  --with-tlib=ncurses \
  --with-compiledby="<admins@wargaming.net>" --enable-cscope \
  --with-modified-by="<admins@wargaming.net>" \
%if "%{withnetbeans}" == "1"
  --enable-netbeans \
%else
  --disable-netbeans \
%endif
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
%if "%{withruby}" == "1"
  --enable-rubyinterp \
%else
  --disable-rubyinterp \
%endif

make VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim gvim
make clean

%configure --prefix=%{_prefix} --with-features=huge \
 --enable-pythoninterp=dynamic \
 --enable-perlinterp \
 --disable-tclinterp \
 --with-x=no \
 --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
 --enable-cscope --with-modified-by="<admins@wargaming.net>" \
 --with-tlib=ncurses \
 --with-compiledby="<admins@wargaming.net>" \
%if "%{withnetbeans}" == "1"
  --enable-netbeans \
%else
  --disable-netbeans \
%endif
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
%if "%{withruby}" == "1"
  --enable-rubyinterp \
%else
  --disable-rubyinterp \
%endif

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}
cp vim enhanced-vim
make clean

perl -pi -e "s/help.txt/vi_help.txt/"  os_unix.h ex_cmds.c
perl -pi -e "s/\/etc\/vimrc/\/etc\/virc/"  feature.h
%configure --prefix=%{_prefix} --with-features=small --with-x=no \
  --enable-multibyte \
  --disable-netbeans \
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
  --disable-pythoninterp --disable-perlinterp --disable-tclinterp \
  --with-tlib=ncurses --enable-gui=no --disable-gpm --exec-prefix=/ \
  --with-compiledby="<admins@wargaming.net>" \
  --with-modified-by="<admins@wargaming.net>"

make VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/bin
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}/vimfiles/{after,autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,syntax_checkers,tutor}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}/vimfiles/after/{autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
%{__tar} xf %{SOURCE24}  -C $RPM_BUILD_ROOT/%{_datadir}/%{name}/vimfiles/
cp -f %{SOURCE11} .
cp -f %{SOURCE14} $RPM_BUILD_ROOT/%{_datadir}/%{name}/vimfiles/template.spec
cp runtime/doc/uganda.txt LICENSE
# Those aren't Linux info files but some binary files for Amiga:
rm -f README*.info


cd src
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
make installgtutorbin  DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64}/apps
install -m755 vim $RPM_BUILD_ROOT%{_bindir}/vi
install -m755 enhanced-vim $RPM_BUILD_ROOT%{_bindir}/vim
install -m755 gvim $RPM_BUILD_ROOT%{_bindir}/gvim

install -p -m644 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/gvim.png
install -p -m644 %{SOURCE8} \
   $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/gvim.png
install -p -m644 %{SOURCE9} \
   $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/gvim.png
install -p -m644 %{SOURCE10} \
   $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps/gvim.png

( cd $RPM_BUILD_ROOT
#  mv ./%{_bindir}/vimtutor ./%{_bindir}/vimtutor
  #mv ./%{_bindir}/vim ./%{_bindir}/vi
  #rm -f ./bin/rvim
  ln -sf vi ./%{_bindir}/ex
  ln -sf vi ./%{_bindir}/rvi
  ln -sf vi ./%{_bindir}/rview
  ln -sf vi ./%{_bindir}/view
  ln -sf vim ./%{_bindir}/ex
  ln -sf vim ./%{_bindir}/rvim
  ln -sf vim ./%{_bindir}/vimdiff
  perl -pi -e "s,$RPM_BUILD_ROOT,," .%{_mandir}/man1/vim.1 .%{_mandir}/man1/vimtutor.1
  rm -f .%{_mandir}/man1/rvim.1
  ln -sf vim.1.gz .%{_mandir}/man1/vi.1.gz
  ln -sf vim.1.gz .%{_mandir}/man1/rvi.1.gz
  ln -sf vim.1.gz .%{_mandir}/man1/vimdiff.1.gz
  ln -sf gvim ./%{_bindir}/gview
  ln -sf gvim ./%{_bindir}/gex
  ln -sf gvim ./%{_bindir}/evim
  ln -sf gvim ./%{_bindir}/gvimdiff
  ln -sf gvim ./%{_bindir}/vimx
  %if "%{desktop_file}" == "1"
    mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
    desktop-file-install --vendor fedora \
        --dir $RPM_BUILD_ROOT/%{_datadir}/applications \
        %{SOURCE3}
        # --add-category "Development;TextEditor;X-Red-Hat-Base" D\
  %else
    mkdir -p ./%{_sysconfdir}/X11/applnk/Applications
    cp %{SOURCE3} ./%{_sysconfdir}/X11/applnk/Applications/gvim.desktop
  %endif
  # ja_JP.ujis is obsolete, ja_JP.eucJP is recommended.
  ( cd ./%{_datadir}/%{name}/%{vimdir}/lang; \
    ln -sf menu_ja_jp.ujis.vim menu_ja_jp.eucjp.vim )
)

pushd $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/tutor
mkdir conv
   iconv -f CP1252 -t UTF8 tutor.ca > conv/tutor.ca
   iconv -f CP1252 -t UTF8 tutor.it > conv/tutor.it
   #iconv -f CP1253 -t UTF8 tutor.gr > conv/tutor.gr
   iconv -f CP1252 -t UTF8 tutor.fr > conv/tutor.fr
   iconv -f CP1252 -t UTF8 tutor.es > conv/tutor.es
   iconv -f CP1252 -t UTF8 tutor.de > conv/tutor.de
   #iconv -f CP737 -t UTF8 tutor.gr.cp737 > conv/tutor.gr.cp737
   #iconv -f EUC-JP -t UTF8 tutor.ja.euc > conv/tutor.ja.euc
   #iconv -f SJIS -t UTF8 tutor.ja.sjis > conv/tutor.ja.sjis
   iconv -f UTF8 -t UTF8 tutor.ja.utf-8 > conv/tutor.ja.utf-8
   iconv -f UTF8 -t UTF8 tutor.ko.utf-8 > conv/tutor.ko.utf-8
   iconv -f CP1252 -t UTF8 tutor.no > conv/tutor.no
   iconv -f ISO-8859-2 -t UTF8 tutor.pl > conv/tutor.pl
   iconv -f ISO-8859-2 -t UTF8 tutor.sk > conv/tutor.sk
   iconv -f KOI8R -t UTF8 tutor.ru > conv/tutor.ru
   iconv -f CP1252 -t UTF8 tutor.sv > conv/tutor.sv
   mv -f tutor.ja.euc tutor.ja.sjis tutor.ko.euc tutor.pl.cp1250 tutor.zh.big5 tutor.ru.cp1251 tutor.zh.euc conv/
   rm -f tutor.ca tutor.de tutor.es tutor.fr tutor.gr tutor.it tutor.ja.utf-8 tutor.ko.utf-8 tutor.no tutor.pl tutor.sk tutor.ru tutor.sv
mv -f conv/* .
rmdir conv
popd

# Dependency cleanups
chmod 644 $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/doc/vim2html.pl \
 $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/tools/*.pl \
 $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/tools/vim132
chmod 644 ../runtime/doc/vim2html.pl

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d
cat >$RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/vim.sh <<EOF
if [ -n "\$BASH_VERSION" -o -n "\$KSH_VERSION" -o -n "\$ZSH_VERSION" ]; then
  [ -x /%{_bindir}/id ] || return
  [ \`/%{_bindir}/id -u\` -le 200 ] && return
  # for bash and zsh, only if no alias is already set
  alias vi >/dev/null 2>&1 || alias vi=vim
fi
EOF
cat >$RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/vim.csh <<EOF
[ -x /%{_bindir}/id ] || exit
[ \`/%{_bindir}/id -u\` -gt 200 ] && alias vi vim
EOF
chmod 0644 $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/*
install -p -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/vimrc
install -p -m644 %{SOURCE5} $RPM_BUILD_ROOT/%{_sysconfdir}/virc
(cd $RPM_BUILD_ROOT/%{_datadir}/%{name}/%{vimdir}/doc;
 gzip -9 *.txt
 gzip -d help.txt.gz version7.txt.gz sponsor.txt.gz
 cp %{SOURCE12} .
 cat tags | sed -e 's/\t\(.*.txt\)\t/\t\1.gz\t/;s/\thelp.txt.gz\t/\thelp.txt\t/;s/\tversion7.txt.gz\t/\tversion7.txt\t/;s/\tsponsor.txt.gz\t/\tsponsor.txt\t/' > tags.new; mv -f tags.new tags
cat >> tags << EOF
vi_help.txt	vi_help.txt	/*vi_help.txt*
vi-author.txt	vi_help.txt	/*vi-author*
vi-Bram.txt	vi_help.txt	/*vi-Bram*
vi-Moolenaar.txt	vi_help.txt	/*vi-Moolenaar*
vi-credits.txt	vi_help.txt	/*vi-credits*
EOF
LANG=C sort tags > tags.tmp; mv tags.tmp tags
 )
(cd ../runtime; rm -rf doc; ln -svf ../../vim/%{vimdir}/doc docs;) 
rm -f $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/macros/maze/maze*.c
rm -rf $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/tools
rm -rf $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/doc/vim2html.pl
rm -f $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/tutor/tutor.gr.utf-8~
( cd $RPM_BUILD_ROOT/%{_mandir}
  for i in `find ??/ -type f`; do
    bi=`basename $i`
    iconv -f latin1 -t UTF8 $i > $RPM_BUILD_ROOT/$bi
    mv -f $RPM_BUILD_ROOT/$bi $i
  done
)

# Remove not UTF-8 manpages
for i in pl.ISO8859-2 it.ISO8859-1 ru.KOI8-R fr.ISO8859-1; do
  rm -rf $RPM_BUILD_ROOT/%{_mandir}/$i
done

# use common man1/ru directory
mv $RPM_BUILD_ROOT/%{_mandir}/ru.UTF-8 $RPM_BUILD_ROOT/%{_mandir}/ru

# Remove duplicate man pages
for i in fr.UTF-8 it.UTF-8 pl.UTF-8; do
  rm -rf $RPM_BUILD_ROOT/%{_mandir}/$i
done

for i in rvim.1 gvim.1 gvimdiff.1; do 
  echo ".so man1/vim.1" > $RPM_BUILD_ROOT/%{_mandir}/man1/$i
done

%post X11
touch --no-create %{_datadir}/icons/hicolor
if [ -x /%{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi
update-desktop-database &> /dev/null ||:

%postun X11
touch --no-create %{_datadir}/icons/hicolor
if [ -x /%{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi
update-desktop-database &> /dev/null ||:

%clean
rm -rf $RPM_BUILD_ROOT

%files common
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/vimrc
%doc README* LICENSE
%doc runtime/docs
%doc Changelog.rpm
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/vimfiles/template.spec
%dir %{_datadir}/%{name}/%{vimdir}
%{_datadir}/%{name}/%{vimdir}/autoload
%{_datadir}/%{name}/%{vimdir}/colors
%{_datadir}/%{name}/%{vimdir}/compiler
%{_datadir}/%{name}/%{vimdir}/doc
%{_datadir}/%{name}/%{vimdir}/*.vim
%{_datadir}/%{name}/%{vimdir}/ftplugin
%{_datadir}/%{name}/%{vimdir}/indent
%{_datadir}/%{name}/%{vimdir}/keymap
%{_datadir}/%{name}/%{vimdir}/lang/*.vim
%{_datadir}/%{name}/%{vimdir}/lang/*.txt
%dir %{_datadir}/%{name}/%{vimdir}/lang
%{_datadir}/%{name}/%{vimdir}/macros
%{_datadir}/%{name}/%{vimdir}/plugin
%{_datadir}/%{name}/%{vimdir}/print
%{_datadir}/%{name}/%{vimdir}/syntax
%{_datadir}/%{name}/%{vimdir}/tutor
%if ! %{withvimspell}
%{_datadir}/%{name}/%{vimdir}/spell
%endif
%lang(af) %{_datadir}/%{name}/%{vimdir}/lang/af
%lang(ca) %{_datadir}/%{name}/%{vimdir}/lang/ca
%lang(cs) %{_datadir}/%{name}/%{vimdir}/lang/cs
%lang(de) %{_datadir}/%{name}/%{vimdir}/lang/de
%lang(en_GB) %{_datadir}/%{name}/%{vimdir}/lang/en_GB
%lang(eo) %{_datadir}/%{name}/%{vimdir}/lang/eo
%lang(es) %{_datadir}/%{name}/%{vimdir}/lang/es
%lang(fi) %{_datadir}/%{name}/%{vimdir}/lang/fi
%lang(fr) %{_datadir}/%{name}/%{vimdir}/lang/fr
%lang(ga) %{_datadir}/%{name}/%{vimdir}/lang/ga
%lang(it) %{_datadir}/%{name}/%{vimdir}/lang/it
%lang(ja) %{_datadir}/%{name}/%{vimdir}/lang/ja
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko.UTF-8
%lang(nb) %{_datadir}/%{name}/%{vimdir}/lang/nb
%lang(no) %{_datadir}/%{name}/%{vimdir}/lang/no
%lang(pl) %{_datadir}/%{name}/%{vimdir}/lang/pl
%lang(pt_BR) %{_datadir}/%{name}/%{vimdir}/lang/pt_BR
%lang(ru) %{_datadir}/%{name}/%{vimdir}/lang/ru
%lang(sk) %{_datadir}/%{name}/%{vimdir}/lang/sk
%lang(sv) %{_datadir}/%{name}/%{vimdir}/lang/sv
%lang(uk) %{_datadir}/%{name}/%{vimdir}/lang/uk
%lang(vi) %{_datadir}/%{name}/%{vimdir}/lang/vi
%lang(zh_CN) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN
%lang(zh_TW) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW
%lang(zh_CN.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN.UTF-8
%lang(zh_TW.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW.UTF-8
%lang(cs.CP1250) %{_datadir}/%{name}/%{vimdir}/lang/cs.cp1250
%lang(ja.euc-jp) %{_datadir}/%{name}/%{vimdir}/lang/ja.euc-jp
%lang(ja.sjis)   %{_datadir}/%{name}/%{vimdir}/lang/ja.sjis
%lang(nl) %{_datadir}/%{name}/%{vimdir}/lang/nl
%lang(pl.UTF-8)  %{_datadir}/%{name}/%{vimdir}/lang/pl.UTF-8
%lang(pl.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/pl.cp1250
%lang(ru.cp1251) %{_datadir}/%{name}/%{vimdir}/lang/ru.cp1251
%lang(uk.cp1251) %{_datadir}/%{name}/%{vimdir}/lang/uk.cp1251
%lang(sk.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/sk.cp1250
%lang(zh_CN.cp936) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN.cp936

/%{_bindir}/xxd
%{_mandir}/man1/vim.*
%{_mandir}/man1/ex.*
%{_mandir}/man1/vi.*
%{_mandir}/man1/view.*
%{_mandir}/man1/rvi.*
%{_mandir}/man1/rview.*
%{_mandir}/man1/xxd.*
%lang(fr) %{_mandir}/fr/man1/*
%lang(it) %{_mandir}/it/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%lang(ru) %{_mandir}/ru/man1/*
%lang(ja) %{_mandir}/ja/man1/*

%if %{withvimspell}
%files spell
%defattr(-,root,root)
%dir %{_datadir}/%{name}/%{vimdir}/spell
%{_datadir}/%{name}/vim70/spell/cleanadd.vim
%lang(af) %{_datadir}/%{name}/%{vimdir}/spell/af.*
%lang(am) %{_datadir}/%{name}/%{vimdir}/spell/am.*
%lang(bg) %{_datadir}/%{name}/%{vimdir}/spell/bg.*
%lang(ca) %{_datadir}/%{name}/%{vimdir}/spell/ca.*
%lang(cs) %{_datadir}/%{name}/%{vimdir}/spell/cs.*
%lang(cy) %{_datadir}/%{name}/%{vimdir}/spell/cy.*
%lang(da) %{_datadir}/%{name}/%{vimdir}/spell/da.*
%lang(de) %{_datadir}/%{name}/%{vimdir}/spell/de.*
%lang(el) %{_datadir}/%{name}/%{vimdir}/spell/el.*
%lang(en) %{_datadir}/%{name}/%{vimdir}/spell/en.*
%lang(eo) %{_datadir}/%{name}/%{vimdir}/spell/eo.*
%lang(es) %{_datadir}/%{name}/%{vimdir}/spell/es.*
%lang(fo) %{_datadir}/%{name}/%{vimdir}/spell/fo.*
%lang(fr) %{_datadir}/%{name}/%{vimdir}/spell/fr.*
%lang(ga) %{_datadir}/%{name}/%{vimdir}/spell/ga.*
%lang(gd) %{_datadir}/%{name}/%{vimdir}/spell/gd.*
%lang(gl) %{_datadir}/%{name}/%{vimdir}/spell/gl.*
%lang(he) %{_datadir}/%{name}/%{vimdir}/spell/he.*
%lang(hr) %{_datadir}/%{name}/%{vimdir}/spell/hr.*
%lang(hu) %{_datadir}/%{name}/%{vimdir}/spell/hu.*
%lang(id) %{_datadir}/%{name}/%{vimdir}/spell/id.*
%lang(it) %{_datadir}/%{name}/%{vimdir}/spell/it.*
%lang(ku) %{_datadir}/%{name}/%{vimdir}/spell/ku.*
%lang(la) %{_datadir}/%{name}/%{vimdir}/spell/la.*
%lang(lt) %{_datadir}/%{name}/%{vimdir}/spell/lt.*
%lang(lv) %{_datadir}/%{name}/%{vimdir}/spell/lv.*
%lang(mg) %{_datadir}/%{name}/%{vimdir}/spell/mg.*
%lang(mi) %{_datadir}/%{name}/%{vimdir}/spell/mi.*
%lang(ms) %{_datadir}/%{name}/%{vimdir}/spell/ms.*
%lang(nb) %{_datadir}/%{name}/%{vimdir}/spell/nb.*
%lang(nl) %{_datadir}/%{name}/%{vimdir}/spell/nl.*
%lang(nn) %{_datadir}/%{name}/%{vimdir}/spell/nn.*
%lang(ny) %{_datadir}/%{name}/%{vimdir}/spell/ny.*
%lang(pl) %{_datadir}/%{name}/%{vimdir}/spell/pl.*
%lang(pt) %{_datadir}/%{name}/%{vimdir}/spell/pt.*
%lang(ro) %{_datadir}/%{name}/%{vimdir}/spell/ro.*
%lang(ru) %{_datadir}/%{name}/%{vimdir}/spell/ru.*
%lang(rw) %{_datadir}/%{name}/%{vimdir}/spell/rw.*
%lang(sk) %{_datadir}/%{name}/%{vimdir}/spell/sk.*
%lang(sl) %{_datadir}/%{name}/%{vimdir}/spell/sl.*
%lang(sv) %{_datadir}/%{name}/%{vimdir}/spell/sv.*
%lang(sw) %{_datadir}/%{name}/%{vimdir}/spell/sw.*
%lang(tet) %{_datadir}/%{name}/%{vimdir}/spell/tet.*
%lang(th) %{_datadir}/%{name}/%{vimdir}/spell/th.*
%lang(tl) %{_datadir}/%{name}/%{vimdir}/spell/tl.*
%lang(tn) %{_datadir}/%{name}/%{vimdir}/spell/tn.*
%lang(uk) %{_datadir}/%{name}/%{vimdir}/spell/uk.*
%lang(yi) %{_datadir}/%{name}/%{vimdir}/spell/yi.*
%lang(yi-tr) %{_datadir}/%{name}/%{vimdir}/spell/yi-tr.*
%lang(zu) %{_datadir}/%{name}/%{vimdir}/spell/zu.*
%endif

%files minimal
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/virc
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvi
%{_bindir}/rview

%files enhanced
%defattr(-,root,root)
%{_bindir}/vim
%{_bindir}/rvim
%{_bindir}/vimdiff
%{_bindir}/vimtutor
%config(noreplace) %{_sysconfdir}/profile.d/vim.*
%{_mandir}/man1/rvim.*
%{_mandir}/man1/vimdiff.*
%{_mandir}/man1/vimtutor.*

%files filesystem
%defattr(-,root,root)
%dir %{_datadir}/%{name}/vimfiles
%dir %{_datadir}/%{name}/vimfiles/after
%dir %{_datadir}/%{name}/vimfiles/autoload
%dir %{_datadir}/%{name}/vimfiles/colors
%dir %{_datadir}/%{name}/vimfiles/compiler
%dir %{_datadir}/%{name}/vimfiles/doc
%dir %{_datadir}/%{name}/vimfiles/ftdetect
%dir %{_datadir}/%{name}/vimfiles/ftplugin
%dir %{_datadir}/%{name}/vimfiles/indent
%dir %{_datadir}/%{name}/vimfiles/keymap
%dir %{_datadir}/%{name}/vimfiles/lang
%dir %{_datadir}/%{name}/vimfiles/plugin
%dir %{_datadir}/%{name}/vimfiles/print
%dir %{_datadir}/%{name}/vimfiles/spell
%dir %{_datadir}/%{name}/vimfiles/syntax
%dir %{_datadir}/%{name}/vimfiles/syntax_checkers
%dir %{_datadir}/%{name}/vimfiles/tutor

%{_datadir}/%{name}/vimfiles/after/**
%{_datadir}/%{name}/vimfiles/autoload/**
%{_datadir}/%{name}/vimfiles/doc/*
%{_datadir}/%{name}/vimfiles/ftdetect/*
%{_datadir}/%{name}/vimfiles/ftplugin/*
%{_datadir}/%{name}/vimfiles/indent/*
%{_datadir}/%{name}/vimfiles/plugin/*
%{_datadir}/%{name}/vimfiles/snippets/*
%{_datadir}/%{name}/vimfiles/syntax/*
%{_datadir}/%{name}/vimfiles/syntax_checkers/**

%files X11
%defattr(-,root,root)
%if "%{desktop_file}" == "1"
/%{_datadir}/applications/*
%else
/%{_sysconfdir}/X11/applnk/*/gvim.desktop
%endif
%{_bindir}/gvimtutor
%{_bindir}/gvim
%{_bindir}/gvimdiff
%{_bindir}/gview
%{_bindir}/gex
%{_bindir}/vimx
%{_bindir}/evim
%{_mandir}/man1/evim.*
%{_mandir}/man1/gvim*
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Thu Jul 31 2014 Ivan Polonevich <joni @ wargaming dot net> - 7.4.389-2
- Update and rebuild for WG

* Thu Oct 17 2013 Vasil Mikhalenya <v_mihalenya at wargaming dot net> 7.4.52
- updated to patchlevel 7.4.52

* Fri Aug 13 2013 Vasil Mikhalenya <v_mihalenya at wargaming dot net> 7.4.0
- updated to version 7.4

* Fri Apr 13 2012 Ivan Polonevich <joni at wargaming dot net> 7.3.138-7
- fix virc

* Fri Feb 24 2012 Ivan Polonevich <joni at wargaming dot net> 7.3.138-3
- add some plugins
- add config

* Thu Feb 17 2012 Ivan Polonevich <joni at wargaming dot net> 7.3.138-2
- build for WG repos

* Thu Mar 17 2011 Karsten Hopp <karsten@redhat.com> 7.3.138-1
- patchlevel 138

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:7.3.107-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Karsten Hopp <karsten@redhat.com> 7.3.107-1
- patchlevel 107

* Mon Jan 10 2011 Karsten Hopp <karsten@redhat.com> 7.3.099-1
- patchlevel 099

* Mon Jan 03 2011 Karsten Hopp <karsten@redhat.com> 7.3.094-1
- patchlevel 094

* Thu Dec 09 2010 Karsten Hopp <karsten@redhat.com> 7.3.081-1
- patchlevel 081

* Wed Dec 08 2010 Karsten Hopp <karsten@redhat.com> 7.3.080-1
- patchlevel 080

* Fri Dec 03 2010 Karsten Hopp <karsten@redhat.com> 7.3.075-1
- patchlevel 075

* Thu Dec 02 2010 Karsten Hopp <karsten@redhat.com> 7.3.073-1
- patchlevel 073

* Thu Nov 25 2010 Karsten Hopp <karsten@redhat.com> 7.3.069-1
- patchlevel 069

* Wed Nov 24 2010 Karsten Hopp <karsten@redhat.com> 7.3.068-1
- patchlevel 068

* Wed Nov 24 2010 Karsten Hopp <karsten@redhat.com> 7.3.063-1
- patchlevel 063

* Wed Nov 17 2010 Karsten Hopp <karsten@redhat.com> 7.3.062-1
- patchlevel 062

* Tue Nov 16 2010 Karsten Hopp <karsten@redhat.com> 7.3.061-1
- patchlevel 061

* Tue Nov 16 2010 Karsten Hopp <karsten@redhat.com> 7.3.056-1
- patchlevel 056

* Thu Nov 11 2010 Karsten Hopp <karsten@redhat.com> 7.3.055-1
- patchlevel 055

* Wed Nov 10 2010 Karsten Hopp <karsten@redhat.com> 7.3.051-1
- patchlevel 051

* Thu Nov 04 2010 Karsten Hopp <karsten@redhat.com> 7.3.050-1
- patchlevel 050

* Thu Nov 04 2010 Karsten Hopp <karsten@redhat.com> 7.3.048-1
- patchlevel 048

* Thu Oct 28 2010 Karsten Hopp <karsten@redhat.com> 7.3.047-1
- patchlevel 047

* Wed Oct 27 2010 Karsten Hopp <karsten@redhat.com> 7.3.046-1
- patchlevel 046

* Wed Oct 27 2010 Karsten Hopp <karsten@redhat.com> 7.3.039-1
- patchlevel 039

* Sun Oct 24 2010 Karsten Hopp <karsten@redhat.com> 7.3.035-1
- patchlevel 035

* Sat Oct 23 2010 Karsten Hopp <karsten@redhat.com> 7.3.034-1
- patchlevel 034

* Sat Oct 23 2010 Karsten Hopp <karsten@redhat.com> 7.3.033-1
- patchlevel 033

* Thu Oct 21 2010 Karsten Hopp <karsten@redhat.com> 7.3.032-1
- patchlevel 032

* Wed Oct 20 2010 Karsten Hopp <karsten@redhat.com> 7.3.031-1
- patchlevel 031

* Sat Oct 16 2010 Karsten Hopp <karsten@redhat.com> 7.3.029-1
- patchlevel 029

* Fri Oct 15 2010 Karsten Hopp <karsten@redhat.com> 7.3.028-1
- patchlevel 028

* Thu Oct 14 2010 Karsten Hopp <karsten@redhat.com> 7.3.027-1
- patchlevel 027

* Wed Oct 13 2010 Karsten Hopp <karsten@redhat.com> 7.3.026-1
- patchlevel 026

* Sun Oct 10 2010 Karsten Hopp <karsten@redhat.com> 7.3.021-1
- patchlevel 021

* Sat Oct 09 2010 Karsten Hopp <karsten@redhat.com> 7.3.020-1
- patchlevel 020

* Fri Oct 01 2010 Karsten Hopp <karsten@redhat.com> 7.3.019-1
- patchlevel 019

* Thu Sep 30 2010 Karsten Hopp <karsten@redhat.com> 7.3.018-1
- patchlevel 018

* Thu Sep 30 2010 Karsten Hopp <karsten@redhat.com> 7.3.011-3
- add filesystem subpackage (#628293)

* Wed Sep 29 2010 jkeating - 2:7.3.011-2
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Karsten Hopp <karsten@redhat.com> 7.3.011-1
- update to VIM 7.3 patchlevel 011

* Tue Jul 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 7.2.446-2
- Rebuild against python 2.7

* Tue Jul 13 2010 Karsten Hopp <karsten@redhat.com> 7.2.446-1
- patchlevel 446

* Thu Jul 08 2010 Karsten Hopp <karsten@redhat.com> 7.2.445-1
- patchlevel 445

* Wed Jun 23 2010 Karsten Hopp <karsten@redhat.com> 7.2.444-2
- rebuild with perl-5.12

* Sun Jun 13 2010 Karsten Hopp <karsten@redhat.com> 7.2.444-1
- patchlevel 444

* Sun Jun 13 2010 Karsten Hopp <karsten@redhat.com> 7.2.443-1
- patchlevel 443

* Sat Jun 05 2010 Karsten Hopp <karsten@redhat.com> 7.2.442-1
- patchlevel 442

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2:7.2.441-2
- Mass rebuild with perl-5.12.0

* Sun May 30 2010 Karsten Hopp <karsten@redhat.com> 7.2.441-1
- patchlevel 441

* Sat May 29 2010 Karsten Hopp <karsten@redhat.com> 7.2.440-1
- patchlevel 440

* Wed May 26 2010 Karsten Hopp <karsten@redhat.com> 7.2.438-1
- patchlevel 438

* Sat May 22 2010 Karsten Hopp <karsten@redhat.com> 7.2.437-1
- patchlevel 437

* Sun May 16 2010 Karsten Hopp <karsten@redhat.com> 7.2.436-1
- patchlevel 436

* Sat May 15 2010 Karsten Hopp <karsten@redhat.com> 7.2.433-1
- patchlevel 433

* Fri May 14 2010 Karsten Hopp <karsten@redhat.com> 7.2.427-1
- patchlevel 427

* Thu May 13 2010 Karsten Hopp <karsten@redhat.com> 7.2.422-1
- patchlevel 422

* Fri May 07 2010 Karsten Hopp <karsten@redhat.com> 7.2.416-1
- patchlevel 416

* Tue Apr 20 2010 Karsten Hopp <karsten@redhat.com> 7.2.411-2
- fix rvim manpage (#583180)

* Wed Mar 24 2010 Karsten Hopp <karsten@redhat.com> 7.2.411-1
- patchlevel 411

* Tue Mar 23 2010 Karsten Hopp <karsten@redhat.com> 7.2.410-1
- patchlevel 410

* Sat Mar 20 2010 Karsten Hopp <karsten@redhat.com> 7.2.403-1
- patchlevel 403

* Thu Mar 18 2010 Karsten Hopp <karsten@redhat.com> 7.2.402-1
- patchlevel 402

* Wed Mar 17 2010 Karsten Hopp <karsten@redhat.com> 7.2.399-1
- patchlevel 399

* Wed Mar 10 2010 Karsten Hopp <karsten@redhat.com> 7.2.394-1
- patchlevel 394

* Wed Mar 03 2010 Karsten Hopp <karsten@redhat.com> 7.2.385-1
- patchlevel 385

* Tue Mar 02 2010 Karsten Hopp <karsten@redhat.com> 7.2.384-1
- patchlevel 384

* Tue Mar 02 2010 Karsten Hopp <karsten@redhat.com> 7.2.381-1
- patchlevel 381

* Sat Feb 27 2010 Karsten Hopp <karsten@redhat.com> 7.2.377-1
- patchlevel 377

* Wed Feb 24 2010 Karsten Hopp <karsten@redhat.com> 7.2.376-1
- patchlevel 376

* Thu Feb 18 2010 Karsten Hopp <karsten@redhat.com> 7.2.368-1
- patchlevel 368

* Thu Feb 18 2010 Karsten Hopp <karsten@redhat.com> 7.2.367-1
- patchlevel 367

* Wed Feb 17 2010 Karsten Hopp <karsten@redhat.com> 7.2.365-1
- patchlevel 365

* Fri Feb 12 2010 Karsten Hopp <karsten@redhat.com> 7.2.359-1
- patchlevel 359

* Thu Feb 11 2010 Karsten Hopp <karsten@redhat.com> 7.2.357-1
- patchlevel 357

* Thu Feb 04 2010 Karsten Hopp <karsten@redhat.com> 7.2.356-1
- patchlevel 356

* Wed Feb 03 2010 Karsten Hopp <karsten@redhat.com> 7.2.354-1
- patchlevel 354

* Fri Jan 29 2010 Karsten Hopp <karsten@redhat.com> 7.2.351-1
- patchlevel 351

* Thu Jan 28 2010 Karsten Hopp <karsten@redhat.com> 7.2.350-1
- patchlevel 350

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2:7.2.315-2
- rebuild against perl 5.10.1

* Wed Dec 03 2009 Karsten Hopp <karsten@redhat.com> 7.2.315-1
- patchlevel 315
- fix vimrc location in man page (#456992)
- correct syntax highlighting of httpd config files in /etc/httpd (#499123)
- Buildrequire ruby, ruby-devel (#503872)
- Remove check for static gravity (#510307)
- sort tags file (#517725)
- use one gvim to open multiple file selections from nautilus (#519265)
- use elinks -source instead of elinks -dump (#518791)
- add ext4 keyword to /etc/fstab syntax highlighting (#498290)

* Mon Nov 09 2009 Karsten Hopp <karsten@redhat.com> 7.2.284-1
- patchlevel 284

* Thu Aug 20 2009 Karsten Hopp <karsten@redhat.com> 7.2.245-3
- change range of system ids in /etc/profile.d/vim/* (#518555)

* Mon Aug 03 2009 Karsten Hopp <karsten@redhat.com> 7.2.245-2
- add fix for glibc fortify segfault (#514717, Adam Tkac)

* Sat Aug 01 2009 Karsten Hopp <karsten@redhat.com> 7.2.245-1
- add 97 upstream patches to get to patchlevel 245

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:7.2.148-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 27 2009 Karsten Hopp <karsten@redhat.com> 7.2.148-1
- patchlevel 148, fixes #461417

* Tue Mar 10 2009 Karsten Hopp <karsten@redhat.com> 7.2.132-1
- patchlevel 132, fixes accesses to freed memory

* Wed Mar 04 2009 Karsten Hopp <karsten@redhat.com> 7.2.131-1
- patchlevel 131

* Tue Feb 24 2009 Karsten Hopp <karsten@redhat.com> 7.2.127-1
- patchlevel 127

* Mon Feb 23 2009 Karsten Hopp <karsten@redhat.com> 7.2.124-1
- patchlevel 124

* Mon Jan 26 2009 Karsten Hopp <karsten@redhat.com> 7.2.088-1
- patchlevel 88

* Thu Jan 08 2009 Karsten Hopp <karsten@redhat.com> 7.2.079-2
- patchlevel 79

* Thu Dec 04 2008 Jesse Keating <jkeating@redhat.com> - 7.2.060-2
- Rebuild for new python.

* Mon Dec 01 2008 Karsten Hopp <karsten@redhat.com> 7.2.060-1
- patchlevel 60

* Mon Nov 10 2008 Karsten Hopp <karsten@redhat.com> 7.2.032-1
- patchlevel 32

* Mon Nov 03 2008 Karsten Hopp <karsten@redhat.com> 7.2.026-2
- add more /usr/share/vim/vimfiles directories (#444387)

* Mon Nov 03 2008 Karsten Hopp <karsten@redhat.com> 7.2.026-1
- patchlevel 26
- own some directories in /usr/share/vim/vimfiles (#469491)

* Tue Oct 21 2008 Karsten Hopp <karsten@redhat.com> 7.2.025-2
- re-enable clean

* Mon Oct 20 2008 Karsten Hopp <karsten@redhat.com> 7.2.025-1
- patchlevel 25
- add Categories tag to desktop file (#226526)
- add requirement on hicolor-icon-theme to vim-X11 (#226526)
- drop Amiga info files (#226526)
- remove non-utf8 man pages (#226526)
- drop Application from categories (#226526)

* Tue Sep 30 2008 Karsten Hopp <karsten@redhat.com> 7.2.022-1
- patchlevel 22

* Mon Sep 08 2008 Karsten Hopp <karsten@redhat.com> 7.2.013-1
- patchlevel 13

* Mon Aug 25 2008 Karsten Hopp <karsten@redhat.com> 7.2.006-1
- patchlevel 6

* Mon Aug 18 2008 Karsten Hopp <karsten@redhat.com> 7.2.002-1
- patchlevel 2
- fix specfile template (#446070)
- old specfile changelog moved to Changelog.rpm

* Fri Aug 14 2008 Karsten Hopp <karsten@redhat.com> 7.2.000-1
- vim 7.2
- drop 330 patches

# vim:nrformats-=octal
