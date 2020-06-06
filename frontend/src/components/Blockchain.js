import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

import Button from 'react-bootstrap/Button'

import Block from './Block'
import { backend, RANGE } from '../config'


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
            <Link to="/">Home</Link>
            <hr />
            <h3>FooChain</h3>
            <div>
                {blockchain.map((block, idx) => <Block key={idx} block={block} />)}
            </div>
            <div>
                {
                    buttons.map(button => {
                        const start = button * RANGE
                        const end = (button+1) * RANGE
                        
                        return (
                            <span key={button} onClick={() => fetchPage({ start, end })}>
                                <Button size="sm" variant="danger">
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