import React, { useState, useEffect } from 'react'

import Button from 'react-bootstrap/Button'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faLink, faSyncAlt, faCaretSquareDown } from '@fortawesome/free-solid-svg-icons'

import Block from './Block'
import { backend, RANGE } from '../config'

import chain from '../assets/chain2.png'


const Blockchain = () => {
    const [blockchain, setblockchain] = useState([])
    const [length, setlength] = useState(0)
    const [slice, setslice] = useState(1)

    const start = slice * RANGE
    const end = (slice+1) * RANGE

    const fetchPage = () => {
        backend.get(`/blockchain/page?start=${start}&end=${end}`)
            .then(response => setblockchain(prevChain => [...prevChain, ...response.data]))

        setslice(slice+1)
    }

    const updateChain = () => {
        backend.get(`/blockchain/page?start=0&end=${RANGE}`)
            .then(response => setblockchain(response.data))

        backend.get('/blockchain/length')
            .then(response => setlength(response.data))

        setslice(1)
    }

    useEffect(() => {
       updateChain()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])


    const MoreButton = () => {
        if (slice<length/RANGE) {
            return (
                <Button variant="outline-light" className="mt-2"
                onClick={() => fetchPage()}>Show more  <FontAwesomeIcon icon={faCaretSquareDown} /></Button>
            )
        }
        return <div className="end">Genesis of the FooChain</div>
    }


    return (
        <div className="Blockchain">
            <h3>FooChain  <FontAwesomeIcon icon={faLink} /></h3>
            <Button variant="outline-light" className="mb-2"
                onClick={() => updateChain()}>Update FooChain  <FontAwesomeIcon icon={faSyncAlt} /></Button>
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