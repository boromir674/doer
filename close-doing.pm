#!/usr/bin/perl

use Time::HiRes ('sleep');

sub close_terminals {
    # Closes all terminals with their titles matching one of ['MPETA', 'GIT', 'IPYTHON', 'SERVER', 'IPython']
    my $terminals = `wmctrl -lx | grep gnome-terminal-server\.Gnome-terminal`;

    # print "TERMINALS\n" . $terminals . "\n";
    # my @ar = split /\n/, $terminals;
    # foreach (@ar) {
    #     my $v = $_;
    #     print "el: $v\n";
    #     if ($v =~ m/G2\s(MPETA|GIT|IPYTHON)/g) {
    #         print "matched $1\n";
    #     }
    # }

    while ($terminals =~ m/G2\s(MPETA|GIT|IPYTHON|SERVER|IPython)/g) {
        # print "matched $1\n";
        close_terminal($1);
    }
}

sub close_terminal {
    # print "in: " . $1 . "\n";
    my $cmd = "wmctrl -c $1 && echo Closed terminal $1";
    # print "cmd: $cmd\n"; 
    system($cmd);
    sleep(0.14);
    # `wmctrl -c -F $1 && echo Closed terminal $1`;
}

close_terminals();
