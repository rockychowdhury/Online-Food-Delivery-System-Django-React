import React from 'react';

const HomePage = () => {
    return (
        <div className='font-accent text-hero bg-neutral-200'>

            <button className="btn-primary text-primary-600">Order Now</button>
            <button className="btn-outline btn-sm text-secondary-600">Add to Cart</button>

            <div className="">
                <div className="p-4">
                    <h3 className="text-subheading text-accent-600">Pizza Margherita</h3>
                    <p className="text-body">Delicious pizza with fresh ingredients</p>
                    <span className="badge-pizza">Pizza</span>
                </div>
            </div>

            <div className="">
                <h1 className=" mb-8">Welcome to QuickFood</h1>
                <div className="grid grid-auto-fit-md gap-6">
                    

                </div>
            </div>


        </div>
    );
};

export default HomePage;