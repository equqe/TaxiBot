import React from 'react'

const CustomButton = ({ width, height, margin, text, icon, backgroundColor, onClick }) => {
  return (
    <button className='btn' 
            onClick={onClick} 
            style={{width: width,
                    height: height,
                    margin: margin,
                    backgroundColor: backgroundColor }}>

        <div className="btn-text"> {text} </div>

        {/* Icon is showed only if it passed as a prop "icon" */}
        { icon !== undefined ? (<img className='btn-icon' src={icon} alt="btn-icon" />):("") }

    </button>
  )
}

export default CustomButton