package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
	"sync"
)

func main() {
	raw, err := ioutil.ReadFile("../day9.txt")
	panicOnError(err)
	prog := parse(string(raw))

	// fmt.Printf("%+v", parse(string(raw)))

	// prog = parse("3,0,4,0,99")
	// prog = parse("1002,4,3,4,33")

	// prog = parse("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
	// prog = parse("1102,34915192,34915192,7,4,7,99,0")
	// prog = parse("104,1125899906842624,99")
	// prog = parse("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99")

	var wg sync.WaitGroup

	cpu0 := newCPU(0, prog, &wg)
	cpu0.chIn <- 2

	go cpu0.run()

	wg.Wait()

	for {
		select {
		case v1 := <-cpu0.chOut:
			println(v1)
		default:
			return
		}
	}

	// prog = parse("3,9,8,9,10,9,4,9,99,-1,8")

	// prog = parse("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10")
	// println(amp(prog, []int{9, 7, 8, 5, 6}))

	// max_v := 0
	// for _, perm := range permutation([]int{9, 7, 8, 5, 6}) {
	// 	v := amp(prog, perm)
	// 	if v > max_v {
	// 		max_v = v
	// 	}
	// }
	// println(max_v)

	// var wg sync.WaitGroup

	// cpu0 := newCPU(0, prog, &wg)
	// cpu0.chIn <- 5

	// go cpu0.run()

	// go func() {
	// 	for {
	// 		v1 := <-cpu0.chOut
	// 		println(v1)
	// 	}
	// }()

	// wg.Wait()

}

func bind(c1 *cpu, c2 *cpu) {
	go func() {
		for {
			//println("xxx")
			v := <-c1.chOut
			c2.chIn <- v
		}
	}()
}

func amp(prog []int, init []int) int {
	var wg sync.WaitGroup

	cpu0 := newCPU(0, prog, &wg)
	cpu0.chIn <- init[0]
	cpu0.chIn <- 0
	go cpu0.run()

	cpu1 := newCPU(1, prog, &wg)
	cpu1.chIn <- init[1]
	bind(cpu0, cpu1)
	go cpu1.run()

	cpu2 := newCPU(2, prog, &wg)
	cpu2.chIn <- init[2]
	bind(cpu1, cpu2)
	go cpu2.run()

	cpu3 := newCPU(3, prog, &wg)
	cpu3.chIn <- init[3]
	bind(cpu2, cpu3)
	go cpu3.run()

	cpu4 := newCPU(4, prog, &wg)
	cpu4.chIn <- init[4]
	bind(cpu3, cpu4)

	bind(cpu4, cpu0)

	go cpu4.run()

	wg.Wait()

	return cpu4.lastOut
}

type cpu struct {
	id      int
	wg      *sync.WaitGroup
	prog    map[int]int
	eip     int
	rbase   int
	chIn    chan int
	chOut   chan int
	lastOut int
}

func newCPU(id int, prog []int, wg *sync.WaitGroup) *cpu {
	wg.Add(1)
	space := make(map[int]int)

	for i, v := range prog {
		space[i] = v
	}

	return &cpu{
		id:    id,
		wg:    wg,
		prog:  space,
		chIn:  make(chan int, 100),
		chOut: make(chan int, 100),
	}
}

type mode int

const (
	position = iota
	immediate
	relative
)

func s(x byte) mode {
	t, _ := strconv.Atoi(string(x))
	return mode(t)
}

func decode(op int) (cd int, p1m mode, p2m mode, p3m mode) {
	sop := fmt.Sprintf("%05d", op)

	p1m = s(sop[2])
	p2m = s(sop[1])
	p3m = s(sop[0])

	cd, err := strconv.Atoi(sop[3:])
	panicOnError(err)

	return
}

func (c *cpu) fetch(addr int, mode mode) int {
	switch mode {
	case position:
		return c.prog[c.prog[addr]]
	case immediate:
		return c.prog[addr]
	case relative:
		return c.prog[c.rbase+c.prog[addr]]
	default:
		panic("unknown mode")
	}
}

func (c *cpu) run() {
	defer c.wg.Done()

	for {
		op, p1m, p2m, p3m := decode(c.prog[c.eip])
		// fmt.Printf("prog %d op %d base %d p1m %d p2m %d p3m %d\n", c.id, op, c.rbase, p1m, p2m, p3m)
		// if p3m == relative {
		// 	fmt.Printf("prog %d op %d base %d p1m %d p2m %d p3m %d\n", c.id, op, c.rbase, p1m, p2m, p3m)
		// }
		c.eip++

		switch op {
		case 1, 2:
			p1 := c.fetch(c.eip+0, p1m)
			p2 := c.fetch(c.eip+1, p2m)
			p3 := c.fetch(c.eip+2, immediate)

			if p3m == relative {
				p3 += c.rbase
			}

			if op == 1 {
				c.prog[p3] = p1 + p2
			} else {
				c.prog[p3] = p1 * p2
			}
			c.eip += 3
		case 3: // input
			p1 := c.fetch(c.eip+0, immediate)

			switch p1m {
			case immediate:
				c.prog[p1] = <-c.chIn
				fmt.Printf("prog %d read %d\n", c.id, c.prog[p1])
			case relative:
				c.prog[c.rbase+p1] = <-c.chIn
				fmt.Printf("prog %d read %d\n", c.id, c.prog[c.rbase+p1])
			default:
				panic("not handled")
			}
			c.eip++
		case 4: // output
			p1 := c.fetch(c.eip+0, p1m)
			fmt.Printf("prog %d output %d\n", c.id, p1)
			c.lastOut = p1
			c.chOut <- p1
			c.eip++
		case 5:
			p1 := c.fetch(c.eip+0, p1m)
			p2 := c.fetch(c.eip+1, p2m)
			if p1 != 0 {
				c.eip = p2
			} else {
				c.eip += 2
			}
		case 6:
			p1 := c.fetch(c.eip+0, p1m)
			p2 := c.fetch(c.eip+1, p2m)
			if p1 == 0 {
				c.eip = p2
			} else {
				c.eip += 2
			}
		case 7:
			p1 := c.fetch(c.eip+0, p1m)
			p2 := c.fetch(c.eip+1, p2m)
			p3 := c.fetch(c.eip+2, immediate)

			if p3m == relative {
				p3 += c.rbase
			}

			if p1 < p2 {
				c.prog[p3] = 1
			} else {
				c.prog[p3] = 0
			}
			c.eip += 3

		case 8:
			p1 := c.fetch(c.eip+0, p1m)
			p2 := c.fetch(c.eip+1, p2m)
			p3 := c.fetch(c.eip+2, immediate)

			if p3m == relative {
				p3 += c.rbase
			}

			if p1 == p2 {
				c.prog[p3] = 1
			} else {
				c.prog[p3] = 0
			}
			c.eip += 3
		case 9:
			p1 := c.fetch(c.eip+0, p1m)
			c.rbase += p1
			c.eip++
		case 99:
			fmt.Printf("prog %d halt\n", c.id)
			// fmt.Printf("prog %d prog\n%v\n", c.id, c.prog)
			return
		default:
			fmt.Printf("wut op: %d", op)
			return
		}
	}
}

func parse(raw string) []int {
	var ops []int
	for _, t := range strings.Split(raw, ",") {
		v, err := strconv.Atoi(t)
		panicOnError(err)
		ops = append(ops, v)
	}

	return ops
}

func panicOnError(err error) {
	if err != nil {
		panic(err)
	}
}

func permutation(xs []int) (permuts [][]int) {
	var rc func([]int, int)
	rc = func(a []int, k int) {
		if k == len(a) {
			permuts = append(permuts, append([]int{}, a...))
		} else {
			for i := k; i < len(xs); i++ {
				a[k], a[i] = a[i], a[k]
				rc(a, k+1)
				a[k], a[i] = a[i], a[k]
			}
		}
	}
	rc(xs, 0)

	return permuts
}
