#!/usr/bin/env python3
"""
Vehicle Data Generator for Python Developer Challenge
This script generates realistic Brazilian vehicle data for database population.
Author: Edgar Damasceno
"""

import argparse
import json
import logging
import math
import random
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from faker import Faker
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn

# Configure logging with rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)
console = Console()


@dataclass
class VehicleProfile:
    """Represents different vehicle market segments"""
    name: str
    price_range: Tuple[float, float]
    depreciation_rate: float
    avg_km_per_year: int
    brands: List[str]


class BrazilianVehicleData:
    """Manages Brazilian vehicle market data and configurations"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize with configuration file or use defaults"""
        self.config = self._load_config(config_path)
        self.faker = Faker('pt_BR')
        self._setup_profiles()
        
    def _load_config(self, config_path: Optional[Path]) -> Dict:
        """Load configuration from YAML file or use defaults"""
        if config_path and config_path.exists():
            logger.info(f"Loading configuration from {config_path}")
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.suffix == '.yaml':
                    return yaml.safe_load(f)
                else:
                    return json.load(f)
        
        logger.info("Using default configuration")
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default Brazilian vehicle market configuration"""
        return {
            'brands_models': {
                # Popular brands
                'Volkswagen': ['Gol', 'Polo', 'Virtus', 'T-Cross', 'Nivus', 'Saveiro', 'Voyage'],
                'Fiat': ['Mobi', 'Argo', 'Cronos', 'Toro', 'Strada', 'Pulse', 'Uno'],
                'Chevrolet': ['Onix', 'Onix Plus', 'Prisma', 'Cruze', 'S10', 'Tracker', 'Spin'],
                'Ford': ['Ka', 'Ka Sedan', 'Fiesta', 'Focus', 'EcoSport', 'Ranger', 'Territory'],
                'Renault': ['Kwid', 'Sandero', 'Logan', 'Duster', 'Captur', 'Oroch'],
                'Hyundai': ['HB20', 'HB20S', 'Creta', 'Tucson', 'Santa Fe'],
                'Toyota': ['Etios', 'Yaris', 'Corolla', 'Hilux', 'SW4', 'RAV4'],
                'Honda': ['Fit', 'City', 'Civic', 'HR-V', 'WR-V', 'CR-V'],
                'Nissan': ['March', 'Versa', 'Kicks', 'Frontier'],
                'Peugeot': ['208', '2008', '3008', '5008'],
                'Citroën': ['C3', 'C4 Cactus', 'C4 Lounge'],
                'Jeep': ['Renegade', 'Compass', 'Commander', 'Wrangler'],
                # Premium brands
                'BMW': ['320i', 'X1', 'X3', 'X5', 'Z4'],
                'Mercedes-Benz': ['C180', 'GLA', 'GLC', 'E-Class'],
                'Audi': ['A3', 'Q3', 'Q5', 'A4'],
                'Volvo': ['XC40', 'XC60', 'XC90']
            },
            'fuel_types': {
                'common': ['flex', 'gasoline'],
                'premium': ['gasoline', 'hybrid'],
                'diesel': ['diesel']
            },
            'colors': {
                'popular': ['Branco', 'Prata', 'Cinza', 'Preto'],
                'common': ['Vermelho', 'Azul', 'Marrom'],
                'premium': ['Branco Pérola', 'Preto Metálico', 'Cinza Grafite']
            },
            'transmissions': {
                'manual': 'manual',
                'automatic': 'automatic',
                'cvt': 'cvt',
                'automated': 'automated_manual'
            }
        }
    
    def _setup_profiles(self):
        """Setup vehicle market segment profiles"""
        self.profiles = {
            'popular': VehicleProfile(
                name='popular',
                price_range=(35000, 80000),
                depreciation_rate=0.18,
                avg_km_per_year=15000,
                brands=['Volkswagen', 'Fiat', 'Chevrolet', 'Ford', 'Renault', 'Hyundai']
            ),
            'intermediate': VehicleProfile(
                name='intermediate',
                price_range=(80000, 150000),
                depreciation_rate=0.15,
                avg_km_per_year=12000,
                brands=['Toyota', 'Honda', 'Nissan', 'Peugeot', 'Citroën', 'Jeep']
            ),
            'premium': VehicleProfile(
                name='premium',
                price_range=(150000, 500000),
                depreciation_rate=0.20,
                avg_km_per_year=10000,
                brands=['BMW', 'Mercedes-Benz', 'Audi', 'Volvo']
            )
        }


class VehicleGenerator:
    """Generates realistic vehicle data based on Brazilian market"""
    
    def __init__(self, data_source: BrazilianVehicleData, seed: Optional[int] = None):
        """Initialize generator with data source and optional seed"""
        self.data = data_source
        if seed is not None:
            random.seed(seed)
            Faker.seed(seed)
        self.current_year = datetime.now().year
        
    def generate_vehicle(self) -> Dict:
        """Generate a single vehicle with realistic attributes"""
        # Choose profile with weighted probability
        profile = self._choose_profile()
        brand = random.choice(profile.brands)
        
        # Ensure brand exists in config
        available_brands = list(self.data.config['brands_models'].keys())
        if brand not in available_brands:
            brand = random.choice(available_brands)
            
        model = random.choice(self.data.config['brands_models'][brand])
        
        # Generate years
        manufacture_year = random.randint(2010, self.current_year - 1)
        model_year = random.choice([manufacture_year, min(manufacture_year + 1, self.current_year)])
        
        # Calculate price and mileage based on age and profile
        age = self.current_year - manufacture_year
        price = self._calculate_price(profile, age)
        mileage = self._calculate_mileage(profile, age)
        
        # Choose other attributes based on profile
        fuel_type = self._choose_fuel_type(profile)
        color = self._choose_color(profile)
        transmission = self._choose_transmission(profile, price)
        engine_size = self._choose_engine_size(profile, model)
        doors = self._choose_doors(model)
        
        return {
            'brand': brand,
            'model': model,
            'manufacture_year': manufacture_year,
            'model_year': model_year,
            'engine_size': engine_size,
            'fuel_type': fuel_type,
            'color': color,
            'mileage': mileage,
            'doors': doors,
            'transmission': transmission,
            'price': price
        }
    
    def _choose_profile(self) -> VehicleProfile:
        """Choose vehicle profile with weighted probability"""
        weights = {'popular': 0.6, 'intermediate': 0.3, 'premium': 0.1}
        return self.data.profiles[random.choices(
            list(weights.keys()),
            weights=list(weights.values())
        )[0]]
    
    def _calculate_price(self, profile: VehicleProfile, age: int) -> float:
        """Calculate realistic price based on profile and depreciation"""
        base_price = random.uniform(*profile.price_range)
        # Exponential depreciation with some randomness
        depreciation_factor = math.exp(-age * profile.depreciation_rate)
        variation = random.uniform(0.9, 1.1)
        final_price = base_price * depreciation_factor * variation
        return round(max(final_price, profile.price_range[0] * 0.3), 2)
    
    def _calculate_mileage(self, profile: VehicleProfile, age: int) -> int:
        """Calculate realistic mileage based on profile and age"""
        base_km = age * profile.avg_km_per_year
        # Add variation: some cars are driven more, some less
        variation = random.uniform(0.5, 1.5)
        return max(0, int(base_km * variation))
    
    def _choose_fuel_type(self, profile: VehicleProfile) -> str:
        """Choose fuel type based on profile"""
        if profile.name == 'popular':
            return random.choice(self.data.config['fuel_types']['common'])
        elif profile.name == 'premium':
            return random.choice(self.data.config['fuel_types']['premium'])
        else:
            all_types = self.data.config['fuel_types']['common'] + ['diesel']
            return random.choice(all_types)
    
    def _choose_color(self, profile: VehicleProfile) -> str:
        """Choose color based on profile and market preferences"""
        if profile.name == 'premium':
            colors = self.data.config['colors']['premium'] + self.data.config['colors']['popular']
        else:
            colors = self.data.config['colors']['popular'] + self.data.config['colors']['common']
        return random.choice(colors)
    
    def _choose_transmission(self, profile: VehicleProfile, price: float) -> str:
        """Choose transmission type based on profile and price"""
        if price < 50000:
            return self.data.config['transmissions']['manual']
        elif price < 100000:
            return random.choice([
                self.data.config['transmissions']['manual'],
                self.data.config['transmissions']['automatic']
            ])
        else:
            return random.choice([
                self.data.config['transmissions']['automatic'],
                self.data.config['transmissions']['cvt']
            ])
    
    def _choose_engine_size(self, profile: VehicleProfile, model: str) -> float:
        """Choose engine size based on vehicle type"""
        if any(truck in model.lower() for truck in ['hilux', 's10', 'ranger', 'toro']):
            return random.choice([2.0, 2.2, 2.8, 3.0])
        elif profile.name == 'popular':
            return random.choice([1.0, 1.3, 1.4])
        elif profile.name == 'premium':
            return random.choice([2.0, 2.5, 3.0])
        else:
            return random.choice([1.4, 1.6, 1.8, 2.0])
    
    def _choose_doors(self, model: str) -> int:
        """Choose number of doors based on model type"""
        two_door_keywords = ['gol', 'ka', 'mobi', 'up']
        if any(keyword in model.lower() for keyword in two_door_keywords):
            return random.choice([2, 4])
        else:
            return random.choice([4, 4, 4, 5])  # Most cars are 4-door


def generate_sql_file(vehicles: List[Dict], output_path: Path) -> None:
    """Generate SQL insert statements for vehicles"""
    logger.info(f"Writing SQL to {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("-- Generated vehicle data for Python Developer Challenge\n")
        f.write(f"-- Generated at: {datetime.now().isoformat()}\n")
        f.write(f"-- Total records: {len(vehicles)}\n\n")
        
        f.write("INSERT INTO vehicles (brand, model, manufacture_year, model_year, ")
        f.write("engine_size, fuel_type, color, mileage, doors, transmission, price) VALUES\n")
        
        values = []
        for v in vehicles:
            value = (
                f"('{v['brand']}', '{v['model']}', {v['manufacture_year']}, "
                f"{v['model_year']}, {v['engine_size']}, '{v['fuel_type']}', "
                f"'{v['color']}', {v['mileage']}, {v['doors']}, "
                f"'{v['transmission']}', {v['price']})"
            )
            values.append(value)
        
        f.write(',\n'.join(values) + ';\n')


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate realistic Brazilian vehicle data for database population',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     # Generate 100 vehicles with defaults
  %(prog)s -n 250             # Generate 250 vehicles
  %(prog)s -c config.yaml     # Use custom configuration
  %(prog)s -o custom.sql      # Output to custom file
  %(prog)s --seed 42          # Use fixed seed for reproducibility
        """
    )
    
    parser.add_argument('-n', '--number', type=int, default=100,
                        help='Number of vehicles to generate (default: 100)')
    parser.add_argument('-o', '--output', type=Path,
                        help='Output SQL file path')
    parser.add_argument('-c', '--config', type=Path,
                        help='Configuration file (YAML or JSON)')
    parser.add_argument('-s', '--seed', type=int,
                        help='Random seed for reproducible results')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Set default output path
    if not args.output:
        output_dir = Path(__file__).parent.parent / "docker" / "postgres" / "init"
        output_dir.mkdir(parents=True, exist_ok=True)
        args.output = output_dir / "02-populate-data.sql"
    
    try:
        # Initialize components
        console.print(f"[bold blue]Vehicle Data Generator[/bold blue]")
        console.print(f"Generating {args.number} vehicles...\n")
        
        data_source = BrazilianVehicleData(args.config)
        generator = VehicleGenerator(data_source, args.seed)
        
        # Generate vehicles with progress bar
        vehicles = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating vehicles...", total=args.number)
            
            for i in range(args.number):
                vehicles.append(generator.generate_vehicle())
                progress.update(task, advance=1)
        
        # Write SQL file
        generate_sql_file(vehicles, args.output)
        
        console.print(f"\n[green]✓[/green] Successfully generated {len(vehicles)} vehicles")
        console.print(f"[green]✓[/green] SQL file written to: {args.output}")
        
        # Show sample statistics
        if args.verbose:
            brands = {}
            for v in vehicles:
                brands[v['brand']] = brands.get(v['brand'], 0) + 1
            
            console.print("\n[bold]Brand Distribution:[/bold]")
            for brand, count in sorted(brands.items(), key=lambda x: -x[1])[:10]:
                console.print(f"  {brand}: {count}")
        
    except Exception as e:
        logger.error(f"Error generating data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()