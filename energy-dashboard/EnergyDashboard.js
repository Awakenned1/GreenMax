import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Building2, Zap, Leaf, DollarSign } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const EnergyDashboard = () => {
  // Sample data - replace with your actual data
  const energyData = [
    { month: 'Jan', consumption: 240, savings: 40 },
    { month: 'Feb', consumption: 220, savings: 45 },
    { month: 'Mar', consumption: 200, savings: 50 },
    // Add more data points as needed
  ];

  const statsCards = [
    {
      title: "Total Consumption",
      value: "2,345 kWh",
      description: "↓ 12% from last month",
      icon: <Zap className="h-6 w-6 text-yellow-500" />
    },
    {
      title: "Energy Savings",
      value: "486 kWh",
      description: "↑ 8% from last month",
      icon: <Leaf className="h-6 w-6 text-green-500" />
    },
    {
      title: "Cost Savings",
      value: "$523.45",
      description: "↑ 15% from last month",
      icon: <DollarSign className="h-6 w-6 text-blue-500" />
    },
    {
      title: "Building Efficiency",
      value: "92%",
      description: "↑ 3% from last month",
      icon: <Building2 className="h-6 w-6 text-purple-500" />
    }
  ];

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Energy Dashboard</h1>
        <div className="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium">
          Live Monitoring
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statsCards.map((card, index) => (
          <Card key={index}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">{card.title}</CardTitle>
              {card.icon}
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{card.value}</div>
              <p className="text-xs text-muted-foreground">{card.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Energy Consumption Trends</CardTitle>
        </CardHeader>
        <CardContent>
          <LineChart
            width={800}
            height={400}
            data={energyData}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="consumption" 
              stroke="#4ade80" 
              strokeWidth={2}
            />
            <Line 
              type="monotone" 
              dataKey="savings" 
              stroke="#60a5fa" 
              strokeWidth={2}
            />
          </LineChart>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Real-time Usage</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {['HVAC', 'Lighting', 'Equipment'].map((system) => (
                <div key={system} className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm font-medium">{system}</span>
                    <span className="text-sm text-muted-foreground">
                      {Math.floor(Math.random() * 100)}%
                    </span>
                  </div>
                  <div className="h-2 bg-gray-100 rounded-full">
                    <div 
                      className="h-2 bg-green-500 rounded-full" 
                      style={{ width: `${Math.floor(Math.random() * 100)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Sustainability Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-center h-[200px]">
              <div className="relative">
                <svg className="w-32 h-32">
                  <circle
                    className="text-gray-200"
                    strokeWidth="12"
                    stroke="currentColor"
                    fill="transparent"
                    r="56"
                    cx="64"
                    cy="64"
                  />
                  <circle
                    className="text-green-500"
                    strokeWidth="12"
                    strokeDasharray={350.8}
                    strokeDashoffset={350.8 * 0.2}
                    strokeLinecap="round"
                    stroke="currentColor"
                    fill="transparent"
                    r="56"
                    cx="64"
                    cy="64"
                  />
                </svg>
                <span className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-2xl font-bold">
                  80%
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default EnergyDashboard;