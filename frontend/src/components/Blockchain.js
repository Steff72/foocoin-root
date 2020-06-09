import React, { useState, useEffect } from 'react'

import Button from 'react-bootstrap/Button'

import Block from './Block'
import { backend, RANGE } from '../config'
import MyNavbar from './Navbar'

import chain from '../assets/chain.png'


const Blockchain = () => {
    const [blockchain, setblockchain] = useState([])
    const [length, setlength] = useState(0)

    const fetchPage = ({ start, end }) => {
        backend.get(`/blockchain/page?start=${start}&end=${end}`)
            .then(response => setblockchain(response.data))
    }

    useEffect(() => {
        fetchPage({ start: 0, end: RANGE })

        backend.get('/blockchain/length')
            .then(response => setlength(response.data))
    }, [])

    const buttons = []
    for (let i=0; i<length/RANGE; i++) {
        buttons.push(i)
    }

    return (
        <div className="Blockchain">
        <MyNavbar />
            <h3>FooChain</h3>
            <div>
                {blockchain.map((block, idx) => (
                    <div>
                        <Block key={idx} block={block} />
                        <img className='Chain' src={chain} alt="chain" />
                    </div>
                ))}
            </div>
            <div>
                {
                    buttons.map(button => {
                        const start = button * RANGE
                        const end = (button+1) * RANGE
                        
                        return (
                            <span key={button} onClick={() => fetchPage({ start, end })}>
                                <Button size="sm" variant="outline-light" className="mt-2">
                                    {button+1}
                                </Button>{' '}
                            </span>
                        )
                    })
                }
            </div>
        </div>
    )
}

export default Blockchain