import React, { useState, useEffect } from 'react'

import Button from 'react-bootstrap/Button'

import Block from './Block'
import { backend, RANGE } from '../config'
import MyNavbar from './Navbar'

import chain from '../assets/chain2.png'


const Blockchain = () => {
    const [blockchain, setblockchain] = useState([])
    const [length, setlength] = useState(0)
    const [slice, setslice] = useState(0)

    const start = slice * RANGE
    const end = (slice+1) * RANGE

    const fetchPage = ({ start, end }) => {
        backend.get(`/blockchain/page?start=${start}&end=${end}`)
            .then(response => setblockchain(prevChain => [...prevChain, ...response.data]))

            
        setslice(slice+1)
    }

    useEffect(() => {
        fetchPage({ start: 0, end: RANGE })

        backend.get('/blockchain/length')
            .then(response => setlength(response.data))
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])


    const MoreButton = () => {
        if (slice<length/RANGE) {
            return (
                <Button variant="outline-light" className="mt-2"
                onClick={() => {
                    fetchPage({ start, end })
                }}>Show more</Button>
            )
        }
        return <div className="end">End of the FooChain</div>
    }


    return (
        <div className="Blockchain">
        <MyNavbar />
            <h3>FooChain</h3>
            <div>
                {blockchain.map((block, idx) => (
                    <div key={idx}>
                        <Block block={block} />
                        <img className='Chain' src={chain} alt="chain" />
                    </div>
                ))}
            </div>
            <MoreButton />
        </div>
    )
}

export default Blockchain